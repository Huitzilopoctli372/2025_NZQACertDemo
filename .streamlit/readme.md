## Enhanced High-Level Flow Diagram (Execution Sequence)
This diagram shows the sequential execution of the stored procedures, including the schema and key parameters passed during the SQL Agent Job execution.

```mermaid
graph TD
    subgraph "SQL Server Agent Job Flow (dw_ods20.portfolio_management)"
        A["Start Job"] --> B{"EXEC BuildProjects @DeliveryScenereoID, @LTPScenereoID"};
        B --> C{"EXEC BuildParentChildHierarchy @DeliveryScenereoID, @LTPScenereoID"};
        C --> D{"EXEC CleanProjects"};
        D --> E{"EXEC BuildBudgets @DeliveryScenereoID, @LTPScenereoID"};
        E --> F{"EXEC CleanBudgets"};
        F --> G{"EXEC UnInflateDeliveryAmounts @InflationPlanName"};
        G --> H{"EXEC BuildCapitalLoans"};
        H --> I{"EXEC RunValidationChecks"};
        I --> J{"EXEC RunMismatchedFieldChecks"};
        J --> K["Job Complete"];
    end
```

## Enhanced Layered Diagram (Processing Stage Grouping)
This view groups objects by their logical processing layer and details the type of operation performed by the stored procedures (e.g., Insert, Update, Recursive Update).

```mermaid
graph TD
    subgraph "Layer 1: Staging/Source (dw_stage_psoda)"
        S_P["Project Table"]
        S_Pr["Program Table"]
        S_K["Key_Project Table"]
        S_I["Inflation_Profile Table"]
        S_B["Budget Source (BudgetInfo/Financials)"]
    end
    subgraph "Layer 2: ODS Projects (dw_ods20)"
        ODS_P["Projects Table"]
        ODS_PCH["ParentChildHierarchy Table"]
    end
    subgraph "Layer 3: ODS Financials (dw_ods20)"
        ODS_B["Budgets Table"]
    end
    subgraph "Layer 4: ODS Validation/Checks (dw_ods20)"
        ODS_V["ValidationChecks Table"]
        ODS_M["MismatchedFields Table"]
    end
    subgraph "Processing Procedures"
        SP1["BuildProjects"]
        SP2["BuildParentChildHierarchy"]
        SP3["CleanProjects"]
        SP4["BuildBudgets"]
        SP5["CleanBudgets"]
        SP6["UnInflateDeliveryAmounts"]
        SP7["BuildCapitalLoans"]
        SP8["RunValidationChecks"]
        SP9["RunMismatchedFieldChecks"]
    end

    S_P & S_Pr --> SP1
    SP1 --> ODS_P("Initial Insert")
    
    S_P & S_Pr --> SP2
    SP2 -- "Insert PCH (Flat Hierarchy)" --> ODS_PCH
    ODS_PCH & ODS_P --> SP2("Recursive CTE for Levels")
    SP2 -- "Update Projects (Hierarchy)" --> ODS_P
    
    ODS_P & S_P & S_K --> SP3("Clean/Transform")
    SP3 --> ODS_P("Delete/Update")
    
    S_B & ODS_P --> SP4("Join/Extract")
    SP4 --> ODS_B("Insert")
    
    ODS_B --> SP5("Tidy")
    SP5 --> ODS_B("Delete/Update")
    
    ODS_B & S_I & ODS_P --> SP6("Un-Inflate")
    SP6 --> ODS_B("Update")
    
    ODS_B --> SP7("Calculate Loans")
    SP7 --> ODS_B("Update")
    
    ODS_P & ODS_B --> SP8("Run Checks")
    SP8 --> ODS_V("Insert Errors")
    
    ODS_P --> SP9("Compare Scenarios")
    SP9 --> ODS_M("Insert Mismatches")
```

## Detailed Column Lineage (Projects Focus)
This lineage details specific transformation functions, focusing on the core fields within the dw_ods20.portfolio_management.Projects table, particularly for scenario-based logic and cleaning.

```mermaid
graph TD
    subgraph "Source: dw_stage_psoda.portfolio_management.Project"
        S_ID["Id"]
        S_Scen["Scenario_ID"]
        S_CF["Custom_Field (JSON)"]
        S_Par["Parent_Project_Obj_Id/Parent_Program_Obj_Id"]
    end

    subgraph "Transformation Logic"
        BP_Logic{"SP: BuildProjects"}
        BPH_Logic{"SP: BuildParentChildHierarchy"}
        CP_Logic{"SP: CleanProjects"}
    end

    subgraph "Target: dw_ods20.portfolio_management.Projects"
        T_ID["ProjectID"]
        T_Src["Source"]
        T_PID["PID"]
        T_CEN["CECodeName"]
        T_CE["CECode"]
        T_P5ID["ParentLevel5ID"]
        T_Path["TreePath"]
    end

    %% BuildProjects Mapping & Initial Transformations
    S_ID --> T_ID("Direct Map")
    S_Scen -- "CASE: @DeliveryScenereoID -> 'Delivery'" --> T_Src
    S_CF -- "LTRIM(JSON_VALUE('$.pid'))" --> T_PID
    S_Par -- "ISNULL(Program/Project ID)" --> T_P5ID
    
    S_CF -- "PARSENAME(REPLACE(JSON_VALUE('$.current_ce_code')))" --> T_CEN("Delivery Logic")
    S_CF -- "JSON_VALUE('$.ltp_current_ce_code')" --> T_CEN("LTP Logic")

    %% Hierarchy Logic (BPH)
    T_P5ID & T_ID --> BPH_Logic
    BPH_Logic -- "Recursive CTE Join" --> T_Path("CONCAT_WS('/', ParentLevel1, ...)")
    
    %% Cleaning Logic (CP)
    T_CEN --> CP_Logic
    CP_Logic -- "LEFT(T.CECodeName, 7/11) WHERE T.CECodeName LIKE 'OLD%'" --> T_CE
    T_Path & T_Name["ProjectName"] -- "REPLACE('&amp;', '&')" --> CP_Logic
    CP_Logic -- "Update" --> T_Name & T_Path
```

## Enhanced Split Diagram: Projects Data Lineage
This diagram details the life cycle of the project data, including initial loading, hierarchy building, cleaning, and eventual scenario comparison and validation.

```mermaid
graph TD
    subgraph "Layer 1: Staging/Source"
        S_P["dw_stage_psoda.portfolio_management.Project"]
        S_Pr["dw_stage_psoda.portfolio_management.Program"]
        S_K["dw_stage_psoda.portfolio_management.Key_Project"]
    end

    subgraph "Layer 2: Projects Building & Transformation"
        BP{"SP: BuildProjects"}
        BPH{"SP: BuildParentChildHierarchy"}
        CP{"SP: CleanProjects"}
        ODS_PCH["dw_ods20.portfolio_management.ParentChildHierarchy"]
        ODS_P["dw_ods20.portfolio_management.Projects"]
    end

    subgraph "Layer 3: Projects Validation"
        RVC{"SP: RunValidationChecks"}
        RMFC{"SP: RunMismatchedFieldChecks"}
        ODS_B["dw_ods20.portfolio_management.Budgets"]
        ODS_V["dw_ods20.portfolio_management.ValidationChecks"]
        ODS_M["dw_ods20.portfolio_management.MismatchedFields"]
    end

    S_P & S_Pr -- "Initial Load, Scenario/PID Mapping" --> BP
    BP -- "INSERT" --> ODS_P
    
    S_P & S_Pr -- "Insert into PCH" --> BPH
    BPH -- "Inserts" --> ODS_PCH
    ODS_PCH & ODS_P -- "Recursive CTE for Hierarchy" --> BPH
    BPH -- "Updates" --> ODS_P("TreePath, Parent Levels")
    
    ODS_P & S_P & S_K -- "CECode Transformation, Key Project Lookup, Dead Row Deletion" --> CP
    CP -- "UPDATE/DELETE" --> ODS_P
    
    ODS_P & ODS_B -- "Validate Project/Budget Consistency (e.g., zero capex checks, funding status)" --> RVC
    RVC -- "Inserts Errors" --> ODS_V
    
    ODS_P -- "Compare Delivery vs LTP Projects (PID Join for Mismatched Fields)" --> RMFC
    RMFC -- "Inserts Mismatches" --> ODS_M
```

## Enhanced Split Diagram: Budget Data Lineage
This diagram details the financial processing path, highlighting the crucial steps of joining to projects, cleaning, applying un-inflation logic, and calculating capital loans.

```mermaid
graph TD
    subgraph "Layer 1: Budget Source & Lookups"
        ODS_P["dw_ods20.portfolio_management.Projects"]
        S_B["Budget/Financial Source Table (BudgetInfo/Financials)"]
        S_I["dw_stage_psoda.portfolio_management.Inflation_Profile"]
    end

    subgraph "Layer 2: Financials Processing & Calculation"
        BB{"SP: BuildBudgets"}
        CB{"SP: CleanBudgets"}
        UIDA{"SP: UnInflateDeliveryAmounts"}
        BCL{"SP: BuildCapitalLoans"}
        ODS_B["dw_ods20.portfolio_management.Budgets"]
    end

    subgraph "Layer 3: Financials Validation"
        RVC{"SP: RunValidationChecks"}
        ODS_V["dw_ods20.portfolio_management.ValidationChecks"]
    end

    S_B & ODS_P -- "Extract/Join Financial Items to Project IDs" --> BB
    BB -- "INSERT" --> ODS_B
    
    ODS_B --> CB
    CB -- "Standardize/Tidy Data" --> ODS_B("UPDATE/DELETE")
    
    ODS_B & S_I & ODS_P -- "Divide Delivery Amounts by Inflation Rate (Inflation_Profile Join)" --> UIDA
    UIDA -- "Updates" --> ODS_B
    
    ODS_B -- "Calculate Capital Loan Revenue/Items" --> BCL
    BCL -- "INSERT/UPDATE" --> ODS_B
    
    ODS_B & ODS_P -- "Check Budget Totals/Status vs Project Status" --> RVC
    RVC -- "Inserts Errors" --> ODS_V
```

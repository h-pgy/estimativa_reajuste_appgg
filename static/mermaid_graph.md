graph TD
    subgraph Preparacao [1. Preparação da Base]
        A[Dados Abertos Dez/2025] --> B[Adição de 30 APPGGs Sintéticos - Nível 1]
    end

    subgraph CalculoBase [2. Diagnóstico da Situação Atual]
        B --> C[Identificar Salário Base Atual por Nível]
        C --> D[Calcular Encargos e Benefícios Atuais]
        D --> E[Totalizar Custo Atual por APPGG]
    end

    subgraph Propostas [3. Aplicação dos Cenários de Reajuste]
        E --> F{Escolha da Proposta}
        F --> G[1.1 Inflação desde Jun/2026]
        F --> H[1.2 Inflação Gestão Nunes desde Jun/2021]
        F --> I[2. Equiparação com AMCI]
    end

    subgraph CalculoProposto [4. Impacto da Proposta]
        G & H & I --> J[Calcular Novo Salário Base por Nível]
        J --> K[Recalcular Encargos e Benefícios]
        K --> L[Totalizar Custo Proposto por APPGG]
    end

    subgraph Consolidacao [5. Consolidação e Projeção]
        L --> M[Calcular Diferença Unitária: Proposto - Atual]
        M --> N[Sumarizar Impacto Mensal por Nível da Carreira]
        N --> O[Simular Progressões - Ciclo 18 meses]
        O --> P[Projeção de Impacto Orçamentário Anual: 2026-2028]
    end

    style Preparacao fill:#f9f,stroke:#333,stroke-width:2px
    style Propostas fill:#bbf,stroke:#333,stroke-width:2px
    style Consolidacao fill:#bfb,stroke:#333,stroke-width:2px
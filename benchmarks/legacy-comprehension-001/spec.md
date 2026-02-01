# Legacy Code Comprehension - Specification

## Objective

Analyze a complex legacy invoice processing codebase and answer questions about its architecture, dependencies, data flow, and business logic.

## Background

You have inherited a legacy Python invoice processing system with no documentation. The system is functional but has accumulated technical debt over time. Your task is to understand the codebase well enough to answer specific questions about how it works.

The system consists of approximately 450 lines of Python code across 6 modules:
- **invoice.py** - Core invoice and invoice item models
- **tax_calculator.py** - Tax calculation logic with regional support
- **payment_processor.py** - Payment gateway integration and processing
- **database.py** - Data persistence layer for invoices and customers
- **workflow.py** - Business process orchestration and approval workflows
- **validators.py** - Invoice and payment method validation logic

## Requirements

### Task Requirements
1. Read and analyze the codebase in `starter-code/`
2. Answer all questions in `questions.json` accurately
3. Write your answers to a file named `answers.json` in the following format:

```json
{
  "answers": [
    {
      "id": 1,
      "answer": "Your detailed answer here..."
    },
    {
      "id": 2,
      "answer": "Your detailed answer here..."
    }
  ]
}
```

### Analysis Guidelines
- You may use any code reading and analysis tools available
- Focus on understanding the actual code behavior, not what you think it should do
- Be specific - reference actual class names, method names, and file names
- Trace dependencies and data flow carefully
- Consider both direct and indirect impacts for change analysis questions

### Time Constraints
- This benchmark is designed to test efficient code exploration
- Recommended time: 30-45 minutes
- Focus on accuracy over speed - wrong answers are heavily penalized

### Quality Requirements
- Answers must be technically accurate based on the code
- Include specific details (class names, method names, constants)
- Explain the "why" behind the design when asked about business logic
- For dependency questions, identify both direct and indirect relationships
- For change impact questions, trace through all affected components

## Success Criteria

Your submission will be considered successful when:
1. You provide answers for all 20 questions
2. Answers demonstrate deep understanding of the codebase
3. Technical details (class/method names, constants) are accurate
4. Dependencies and data flows are correctly traced
5. Impact analysis identifies all affected components

## Deliverables

1. **answers.json** - Your answers to all questions in the specified format
2. All answers must be based on actual code analysis, not assumptions

## Evaluation

Your submission will be scored on:
- **Q&A Accuracy** (40%) - Correctness of answers, matching expected keywords
- **Dependency Mapping** (30%) - Correctly identifying module relationships
- **Impact Analysis** (20%) - Accurately predicting what breaks when changes are made
- **Analysis Quality** (10%) - Clarity and completeness of explanations

See `verification/verify.sh` for automated scoring implementation.

## Notes

- This is legacy code with some technical debt, but it is functional
- Don't assume the code follows best practices - analyze what's actually there
- Some design decisions may seem odd - that's realistic for legacy systems
- Pay attention to subtle details like local imports vs module-level imports
- The cache mechanism, status transitions, and error handling all have implications

Before making ANY changes to the SARA project, follow these rules strictly:

1. **INSPECT FIRST, MODIFY SECOND**

   * Read and understand the existing project structure and relevant files before writing code.
   * Do NOT assume a file, function, class, variable, schema, or dependency exists.
   * Do NOT create a new file if the existing architecture can support the requirement cleanly.
   * Do NOT rewrite working code just to make it "cleaner."

2. **PRESERVE THE WORKING CORE**
   The following SARA pipeline is already implemented and working successfully:
   AURA → NEXA → LYRA → ITHRA → Multi-Agent Debate → Consensus → Final Synthesis.

   Treat this core as stable.
   Do NOT modify its logic unless an API integration genuinely requires a change.

3. **THINK BEFORE EVERY CHANGE**
   Before adding a line of code, ask:

   * Is this actually necessary?
   * Does this functionality already exist somewhere?
   * Can I reuse an existing function/class/schema?
   * Will this introduce duplicate logic?
   * Does this change break the current pipeline?
   * Is there a simpler solution?

4. **MINIMAL CODE PRINCIPLE**
   Write the minimum amount of code required to accomplish the task.
   Avoid:

   * unnecessary abstractions
   * unnecessary helper functions
   * duplicate validation
   * duplicate schemas
   * unused imports
   * speculative features
   * premature optimization
   * unnecessary comments
   * unnecessary dependencies

5. **FOLLOW THE EXISTING ARCHITECTURE**
   First understand how the current SARA modules communicate.
   The API layer should CALL the existing orchestration/pipeline rather than duplicate its logic.

6. **NO UNREQUESTED FEATURES**
   Do not add authentication, databases, caching, WebSockets, background workers, logging frameworks, Docker configuration, frontend code, or other features unless explicitly requested or clearly required by the current task.

7. **DEPENDENCIES**
   Before adding a package:

   * Check whether the functionality already exists in the current dependencies.
   * Prefer the standard library or existing dependencies where practical.
   * Do not add a dependency for a trivial task.

8. **ERROR HANDLING**
   Add error handling only where it provides meaningful protection.
   Do not wrap every line in try/except.
   Do not silently swallow exceptions.
   Preserve useful error information.

9. **API DESIGN**
   Keep the API layer thin:
   Request → validation → existing SARA pipeline → structured response.

   Do not move business logic into the API routes.

10. **BEFORE CODING**
    Briefly tell me:

    * which existing files you inspected
    * what you intend to change
    * why each change is necessary
    * which files you will NOT change and why

    Then wait for approval before making substantial modifications.

11. **AFTER CODING**
    Report:

    * files changed
    * what was changed
    * why it was necessary
    * tests performed
    * whether the existing SARA pipeline still works

12. **QUALITY CHECK**
    Before finishing, inspect your own changes for:

    * unused imports
    * dead code
    * duplicate logic
    * unnecessary abstractions
    * unnecessary files
    * inconsistent naming
    * broken imports
    * changes to working functionality that were not required.

**Core principle:**
Do not write code because you *can* write it.
Write code only when you can explain exactly **why that line, function, file, or dependency is necessary.**

If an existing implementation can be reused, REUSE IT.
If a change is not necessary, DON'T MAKE IT.
If you are unsure, STOP and ask rather than guessing.
# Generate Product Spec

Take the user's product description and generate a comprehensive SPEC.md file.

## Steps

1. Ask the user to describe their product idea (or read from the argument: $ARGUMENTS)
2. Generate a SPEC.md with the following sections:
   - **Product Name & Description**: One-paragraph summary
   - **Core Features**: Bulleted list of MVP features
   - **Data Model**: Tables with columns, types, and relationships
   - **API Endpoints**: REST endpoints with methods, paths, request/response schemas
   - **Pages & Components**: Frontend pages with key components and their data needs
   - **Auth Rules**: Which endpoints/pages require auth, any role-based access
   - **Optional Layers**: Which of the 10 optional layers this product needs (qdrant, stripe, resend, etc.)
   - **Environment Variables**: Additional env vars beyond the template defaults
3. Write the SPEC.md to the project root
4. Ask the user to review and iterate — refine sections based on feedback
5. Mark the spec as final when the user approves

## Output
A complete SPEC.md at the project root that the `/build-from-spec` command can consume.

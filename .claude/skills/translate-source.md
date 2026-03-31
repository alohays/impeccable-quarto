---
name: translate-source
description: "Convert any source material to slide content (PDF, markdown, text, URL)"
user-invocable: true
argument-hint: "[source] [format]"
---

# /translate-source — Source Material Translation

[MANDATORY PREPARATION]
- Read `.claude/rules/source-translation.md` for conversion rules per source type
- Read `.claude/rules/design-standards.md` for slide content constraints
- Identify the source type (PDF, markdown, plain text, URL, image)
- Read or fetch the source material completely
- Determine the target format (Quarto RevealJS `.qmd` by default)

[IMPLEMENTATION STEPS]
1. **Source Identification & Ingestion**
   - PDF: Read using PDF tool, extract text, figures, and structure
   - Markdown: Parse headings, content blocks, code blocks
   - Plain text: Identify structure, key points, logical breaks
   - URL: Fetch content, extract main body text
   - Image: Describe content, extract any visible text/data

2. **Content Extraction**
   - **Papers**: Core contribution (1-2 sentences), methodology (simplified), key results (3-5 findings), key figures/tables, limitations, conclusion
   - **Documents**: Executive summary, key sections, important data points, action items
   - **Outlines**: Hierarchy of topics, suggested depth per section
   - **Raw text**: Identify themes, group related points, find a narrative thread

3. **Slide-Ready Transformation**
   - Apply 1-idea-per-slide rule
   - Convert paragraphs to key phrases (move details to speaker notes)
   - Identify what needs visual representation vs. text
   - Suggest diagram/chart types for data
   - Create section groupings

4. **Output Generation**
   - Generate `.qmd` content with proper Quarto/RevealJS syntax
   - Include YAML frontmatter appropriate for the content type
   - Add speaker notes with expanded context from source
   - Mark places where images/diagrams should be created with `<!-- TODO: [description] -->`
   - Include source citations/references

5. **Quality Check**
   - Verify all key information from source is preserved (in slides or notes)
   - Check that no critical data was lost in translation
   - Ensure the output tells a coherent story
   - Validate Quarto syntax

[ANTI-PATTERNS TO AVOID]
- Do NOT copy-paste source text directly onto slides
- Do NOT lose important nuance or caveats when simplifying
- Do NOT create slides without speaker notes containing the detailed context
- Do NOT ignore figures/tables from the source — these often make the best slides
- Do NOT assume one source structure maps to one slide structure

[QUALITY CHECKS]
- All key information from source is present (in slides or speaker notes)
- Each slide has one clear idea
- Speaker notes contain expanded context
- TODO markers exist for needed visuals
- Output compiles as valid Quarto
- Source is properly cited/attributed

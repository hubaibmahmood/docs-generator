import { GoogleGenAI } from "@google/genai";

// Initialize Gemini Client
const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

const MODEL_FAST = 'gemini-2.5-flash';
const MODEL_SMART = 'gemini-2.5-flash'; // Using flash for speed in demo, typically pro for reasoning

export const generateProjectOverview = async (fileStructure: string, dependencies: string): Promise<string> => {
  try {
    const response = await ai.models.generateContent({
      model: MODEL_SMART,
      contents: `You are a senior technical writer.
      Analyze this project structure and dependency list.
      Generate a comprehensive "Project Overview" in Markdown.
      
      Include:
      1. What the project likely does (infer from names and deps).
      2. Tech Stack detected.
      3. Key Features (inferred).
      4. A "Getting Started" guide assuming standard scripts.
      
      Project Structure:
      ${fileStructure}
      
      Dependencies:
      ${dependencies}
      `,
      config: {
        systemInstruction: "Output strictly Markdown. Be professional and concise.",
      }
    });
    return response.text || "Failed to generate overview.";
  } catch (error) {
    console.error("Gemini Overview Error:", error);
    return "## Error Generating Overview\n\nCould not connect to AI service.";
  }
};

export const generateFileDocumentation = async (fileName: string, codeContent: string): Promise<string> => {
  try {
    const response = await ai.models.generateContent({
      model: MODEL_FAST,
      contents: `Analyze this code file named "${fileName}" and generate documentation.
      
      Output Format (Markdown):
      # [File Name]
      
      ## Purpose
      [Brief description]
      
      ## Key Components/Functions
      [List main functions/classes with inputs/outputs]
      
      ## Usage Example
      \`\`\`typescript
      // Example code
      \`\`\`
      
      Code to Analyze:
      ${codeContent.substring(0, 30000)} // Limit context for demo safety
      `,
    });
    return response.text || "No documentation generated.";
  } catch (error) {
    console.error("Gemini File Doc Error:", error);
    return `## Error\n\nFailed to analyze ${fileName}.`;
  }
};

export const generateArchitectureDocs = async (fileTree: string): Promise<string> => {
  try {
    const response = await ai.models.generateContent({
      model: MODEL_FAST,
      contents: `Create an Architecture Overview based on this file tree.
      Use Mermaid JS diagrams (wrapped in \`\`\`mermaid \`\`\`) to visualize relationships between likely modules.
      Explain the data flow.
      
      File Tree:
      ${fileTree}
      `,
    });
    return response.text || "Failed to generate architecture.";
  } catch (error) {
    console.error("Gemini Arch Error:", error);
    return "## Error\n\nFailed to generate architecture docs.";
  }
};

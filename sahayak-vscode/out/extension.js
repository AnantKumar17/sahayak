"use strict";
// import * as vscode from 'vscode';
// import axios from 'axios';
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
// let lastAIReview: string | null = null; // Store the last AI review
// export function activate(context: vscode.ExtensionContext) {
//     let reviewCommand = vscode.commands.registerCommand('sahayak.reviewCode', async () => {
//         const editor = vscode.window.activeTextEditor;
//         if (editor) {
//             const selection = editor.selection;
//             const code = editor.document.getText(selection);
//             if (!code.trim()) {
//                 vscode.window.showErrorMessage("Please select some code before running the review.");
//                 return;
//             }
//             vscode.window.showInformationMessage("Fetching AI review...");
//             try {
//                 const response = await axios.post('http://127.0.0.1:8000/review', { code });
//                 if (response.status === 200 && response.data) {
//                     const aiReview = response.data;
//                     const languageId = editor.document.languageId;
//                     let commentPrefix: string;
//                     if (["python", "shellscript"].includes(languageId)) {
//                         commentPrefix = "# ";
//                     } else if (["javascript", "typescript", "java", "c", "cpp", "go", "rust"].includes(languageId)) {
//                         commentPrefix = "// ";
//                     } else {
//                         commentPrefix = "/* ";
//                     }
//                     let commentText = `
// ${commentPrefix} AI Review:
// ${commentPrefix} - Readability: ${aiReview.readability || "No data"}
// ${commentPrefix} - Security: ${aiReview.security || "No data"}
// ${commentPrefix} - Performance: ${aiReview.performance || "No data"}
// ${commentPrefix} - Best Practices: ${aiReview["best practices"] || "No data"}
// ${commentPrefix} - Bugs: ${aiReview.bugs || "No data"}
// ${commentPrefix} - Overall Analysis: ${aiReview["overall analysis"] || "No data"}
// ${commentPrefix} - Suggested Refactored Code:
// ${(aiReview["suggested refactored code"] || "No data").split("\n").map((line: string) => commentPrefix + " " + line).join("\n")}
// `;
//                     if (commentPrefix === "/* ") {
//                         commentText = `/*
//  AI Review:
// - Readability: ${aiReview.readability || "No data"}
// - Security: ${aiReview.security || "No data"}
// - Performance: ${aiReview.performance || "No data"}
// - Best Practices: ${aiReview["best practices"] || "No data"}
// - Bugs: ${aiReview.bugs || "No data"}
// - Overall Analysis: ${aiReview["overall analysis"] || "No data"}
// - Suggested Refactored Code:
// ${(aiReview["suggested refactored code"] || "No data").split("\n").map((line: string) => "  " + line).join("\n")}
// */`;
//                     }
//                     lastAIReview = commentText; // Store the review for follow-up
//                     const edit = new vscode.WorkspaceEdit();
//                     const position = new vscode.Position(selection.end.line + 3, 0);
//                     edit.insert(editor.document.uri, position, commentText);
//                     await vscode.workspace.applyEdit(edit);
//                     vscode.window.showInformationMessage("AI review added as inline comment. Use 'Sahayak: Follow-up on Review' for further improvements.");
//                 } else {
//                     vscode.window.showErrorMessage("API response format unexpected. Check console.");
//                 }
//             } catch (error: any) {
//                 console.error("Error fetching AI review:", error);
//                 vscode.window.showErrorMessage("Error fetching AI review: " + error.message);
//             }
//         }
//     });
// //     let followupCommand = vscode.commands.registerCommand('sahayak.followup', async () => {
// //         if (!lastAIReview) {
// //             vscode.window.showErrorMessage("No AI review found. Please run 'Sahayak: Review Code' first.");
// //             return;
// //         }
// //         await vscode.env.clipboard.writeText(lastAIReview); // Copy AI review to clipboard
// //         vscode.window.showInformationMessage("AI review copied. Now enter your follow-up question.");
// //         const question = await vscode.window.showInputBox({ prompt: "Enter your follow-up question for the AI review:" });
// //         if (!question) {
// //             vscode.window.showErrorMessage("Follow-up question was empty.");
// //             return;
// //         }
// //         vscode.window.showInformationMessage("Fetching AI follow-up response...");
// //         try {
// //             const response = await axios.post('http://127.0.0.1:8000/followup', { review: lastAIReview, question: question });
// //             if (response.status === 200 && response.data) {
// //                 let followupResponse = response.data || "No response received.";
// //                 const editor = vscode.window.activeTextEditor;
// //                 if (editor) {
// //                     const selection = editor.selection;
// //                     const edit = new vscode.WorkspaceEdit();
// //                     const position = new vscode.Position(selection.end.line + 2, 0);
// //                     let commentPrefix = editor.document.languageId === "python" ? "# " : "// ";
// // //                     let followupComment = `
// // // ${commentPrefix} AI Follow-up:
// // // ${commentPrefix} ${followupResponse.split("\n").map((line: string) => commentPrefix + " " + line).join("\n")}
// // // `;
// //                     let followupComment = "";
// //                     if (typeof followupResponse !== "string") {
// //                         followupResponse = JSON.stringify(followupResponse, null, 2); // Convert object to readable string
// //                     }
// //                     if(followupResponse["suggested refactored code"]) {
// //                     followupComment = `
// // ${commentPrefix} AI Follow-up:
// // ${followupResponse.split("\n").map((line: string) => commentPrefix + " " + line).join("\n")}
// // ${(followupResponse["suggested refactored code"] || "No data").split("\n").map((line: string) => commentPrefix + " " + line).join("\n")}
// // `;
// //                     }
// //                     else{
// //                     followupComment = `
// // ${commentPrefix} AI Follow-up:
// // ${followupResponse.split("\n").map((line: string) => commentPrefix + " " + line).join("\n")}
// // `;
// //                     }
// //                     edit.insert(editor.document.uri, position, followupComment);
// //                     await vscode.workspace.applyEdit(edit);
// //                 }
// //                 vscode.window.showInformationMessage("Follow-up response added as an inline comment.");
// //             } else {
// //                 vscode.window.showErrorMessage("Error in follow-up API response.");
// //             }
// //         } catch (error: any) {
// //             console.error("Error fetching follow-up:", error);
// //             vscode.window.showErrorMessage("Error fetching follow-up: " + error.message);
// //         }
// //     });
// //     context.subscriptions.push(reviewCommand);
// //     context.subscriptions.push(followupCommand);
// let followupCommand = vscode.commands.registerCommand('sahayak.followup', async () => {
//     if (!lastAIReview) {
//         vscode.window.showErrorMessage("No AI review found. Please run 'Sahayak: Review Code' first.");
//         return;
//     }
//     await vscode.env.clipboard.writeText(lastAIReview); // Copy AI review to clipboard
//     vscode.window.showInformationMessage("AI review copied. Now enter your follow-up question.");
//     const question = await vscode.window.showInputBox({ prompt: "Enter your follow-up question for the AI review:" });
//     if (!question) {
//         vscode.window.showErrorMessage("Follow-up question was empty.");
//         return;
//     }
//     vscode.window.showInformationMessage("Fetching AI follow-up response...");
//     try {
//         const response = await axios.post('http://127.0.0.1:8000/followup', { review: lastAIReview, question: question });
//         if (response.status === 200 && response.data) {
//             const followupData = response.data; // Expecting JSON format
//             if (!followupData.response) {
//                 vscode.window.showErrorMessage("Invalid AI follow-up response format.");
//                 return;
//             }
//             const editor = vscode.window.activeTextEditor;
//             if (editor) {
//                 const selection = editor.selection;
//                 const edit = new vscode.WorkspaceEdit();
//                 const position = new vscode.Position(selection.end.line + 7, 0);
//                 let commentPrefix = editor.document.languageId === "python" ? "# " : "// ";
//                 // Format the AI follow-up response
//                 let followupComment = `\n\n${commentPrefix} AI Follow-up:\n`;
//                 // followupComment += `${commentPrefix} ${followupData.response.split("\n").map((line: string) => commentPrefix + " " + line).join("\n")}\n`;
//                 followupComment += followupData.response
//                     .split("\n")
//                     .map((line: string) => 
//                         line.startsWith(commentPrefix.trim()) ? `${commentPrefix} ${line.trim()}` : `${commentPrefix} ${line}`
//                     )
//                     .join("\n") + "\n";
//                 // Handle suggested refactored code if present
//                 if (followupData["suggested refactored code"]) {
//                     followupComment += `\n${commentPrefix} Suggested Refactored Code:\n`;
//                     // Properly format the refactored code as an inline comment
//                     const refactoredCodeLines = followupData["suggested refactored code"].split("\n");
//                     refactoredCodeLines.forEach((line: string) => {
//                         followupComment += `${commentPrefix} ${line}\n`;
//                     });
//                 }
//                 edit.insert(editor.document.uri, position, followupComment);
//                 await vscode.workspace.applyEdit(edit);
//             }
//             vscode.window.showInformationMessage("Follow-up response added as an inline comment.");
//         } else {
//             vscode.window.showErrorMessage("Error in follow-up API response.");
//         }
//     } catch (error: any) {
//         console.error("Error fetching follow-up:", error);
//         vscode.window.showErrorMessage("Error fetching follow-up: " + error.message);
//     }
// });
// context.subscriptions.push(reviewCommand);
// context.subscriptions.push(followupCommand);
// }
// export function deactivate() {}
const vscode = __importStar(require("vscode"));
const axios_1 = __importDefault(require("axios"));
let lastAIReview = null;
function activate(context) {
    let reviewCommand = vscode.commands.registerCommand('sahayak.reviewCode', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage("No active editor found.");
            return;
        }
        const selection = editor.selection;
        const code = editor.document.getText(selection);
        if (!code.trim()) {
            vscode.window.showErrorMessage("Please select some code before running the review.");
            return;
        }
        const prNumberInput = await vscode.window.showInputBox({
            prompt: "Enter GitHub PR number (optional, press Enter to skip):",
            placeHolder: "e.g., 1 (or leave blank)"
        });
        if (prNumberInput === undefined) {
            vscode.window.showErrorMessage("Review cancelled. PR number prompt was dismissed.");
            return;
        }
        const prNumber = prNumberInput ? parseInt(prNumberInput) : undefined;
        if (prNumberInput) {
            if (isNaN(Number(prNumberInput)) || prNumber <= 0) {
                vscode.window.showErrorMessage("Invalid PR number. Please enter a valid positive integer.");
                return;
            }
        }
        vscode.window.showInformationMessage("Fetching AI review...");
        try {
            const response = await axios_1.default.post('http://127.0.0.1:8000/review', {
                code,
                pr_number: prNumber
            });
            if (response.status === 200 && response.data) {
                const aiReview = response.data;
                const languageId = editor.document.languageId;
                let commentPrefix;
                if (["python", "shellscript"].includes(languageId)) {
                    commentPrefix = "# ";
                }
                else if (["javascript", "typescript", "java", "c", "cpp", "go", "rust"].includes(languageId)) {
                    commentPrefix = "// ";
                }
                else {
                    commentPrefix = "/* ";
                }
                let commentText = `
${commentPrefix} AI Review:
${commentPrefix} - Readability: ${aiReview.readability || "No data"}
${commentPrefix} - Security: ${aiReview.security || "No data"}
${commentPrefix} - Performance: ${aiReview.performance || "No data"}
${commentPrefix} - Best Practices: ${aiReview["best practices"] || "No data"}
${commentPrefix} - Bugs: ${aiReview.bugs || "No data"}
${commentPrefix} - Overall Analysis: ${aiReview["overall analysis"] || "No data"}
${commentPrefix} - Suggested Refactored Code:
${(aiReview["suggested refactored code"] || "No data").split("\n").map((line) => commentPrefix + " " + line).join("\n")}
`;
                if (commentPrefix === "/* ") {
                    commentText = `/*
 AI Review:
- Readability: ${aiReview.readability || "No data"}
- Security: ${aiReview.security || "No data"}
- Performance: ${aiReview.performance || "No data"}
- Best Practices: ${aiReview["best practices"] || "No data"}
- Bugs: ${aiReview.bugs || "No data"}
- Overall Analysis: ${aiReview["overall analysis"] || "No data"}
- Suggested Refactored Code:
${(aiReview["suggested refactored code"] || "No data").split("\n").map((line) => "  " + line).join("\n")}
*/`;
                }
                lastAIReview = commentText;
                const edit = new vscode.WorkspaceEdit();
                const position = new vscode.Position(selection.end.line + 3, 0);
                edit.insert(editor.document.uri, position, commentText);
                await vscode.workspace.applyEdit(edit);
                vscode.window.showInformationMessage("AI review added as inline comment. Use 'Sahayak: Follow-up on Review' for further improvements.");
            }
            else {
                vscode.window.showErrorMessage("API response format unexpected. Check console.");
            }
        }
        catch (error) {
            console.error("Error fetching AI review:", error);
            vscode.window.showErrorMessage("Error fetching AI review: " + error.message);
        }
    });
    let followupCommand = vscode.commands.registerCommand('sahayak.followup', async () => {
        if (!lastAIReview) {
            vscode.window.showErrorMessage("No AI review found. Please run 'Sahayak: Review Code' first.");
            return;
        }
        await vscode.env.clipboard.writeText(lastAIReview);
        vscode.window.showInformationMessage("AI review copied. Now enter your follow-up question.");
        const question = await vscode.window.showInputBox({ prompt: "Enter your follow-up question for the AI review:" });
        if (!question) {
            vscode.window.showErrorMessage("Follow-up question was empty.");
            return;
        }
        vscode.window.showInformationMessage("Fetching AI follow-up response...");
        try {
            const response = await axios_1.default.post('http://127.0.0.1:8000/followup', { review: lastAIReview, question: question });
            if (response.status === 200 && response.data) {
                const followupData = response.data;
                if (!followupData.response) {
                    vscode.window.showErrorMessage("Invalid AI follow-up response format.");
                    return;
                }
                const editor = vscode.window.activeTextEditor;
                if (editor) {
                    const selection = editor.selection;
                    const edit = new vscode.WorkspaceEdit();
                    const position = new vscode.Position(selection.end.line + 7, 0);
                    let commentPrefix = editor.document.languageId === "python" ? "# " : "// ";
                    let followupComment = `\n\n${commentPrefix} AI Follow-up:\n`;
                    followupComment += followupData.response
                        .split("\n")
                        .map((line) => line.startsWith(commentPrefix.trim()) ? `${commentPrefix} ${line.trim()}` : `${commentPrefix} ${line}`)
                        .join("\n") + "\n";
                    if (followupData["suggested refactored code"]) {
                        followupComment += `\n${commentPrefix} Suggested Refactored Code:\n`;
                        const refactoredCodeLines = followupData["suggested refactored code"].split("\n");
                        refactoredCodeLines.forEach((line) => {
                            followupComment += `${commentPrefix} ${line}\n`;
                        });
                    }
                    edit.insert(editor.document.uri, position, followupComment);
                    await vscode.workspace.applyEdit(edit);
                }
                vscode.window.showInformationMessage("Follow-up response added as an inline comment.");
            }
            else {
                vscode.window.showErrorMessage("Error in follow-up API response.");
            }
        }
        catch (error) {
            console.error("Error fetching follow-up:", error);
            vscode.window.showErrorMessage("Error fetching follow-up: " + error.message);
        }
    });
    context.subscriptions.push(reviewCommand);
    context.subscriptions.push(followupCommand);
}
function deactivate() { }
//# sourceMappingURL=extension.js.map
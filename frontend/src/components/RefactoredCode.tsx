// src/components/RefactoredCode.tsx
function RefactoredCode({ code }: { code: string }) {
  return (
    <div className="refactored-code">
      <h3>Refactored Code</h3>
      <pre>{code}</pre>
    </div>
  );
}

export default RefactoredCode;
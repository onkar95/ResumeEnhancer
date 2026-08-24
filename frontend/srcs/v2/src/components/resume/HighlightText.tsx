import { diffWords } from "../../utils/resumeDiff";

interface Props {
  original?: string;
  current?: string;
  /** When false, renders plain text with no diffing at all. */
  diff?: boolean;
}

export default function HighlightText({
  original = "",
  current = "",
  diff = true,
}: Props) {
  if (!diff) {
    return <>{current}</>;
  }

  const tokens = diffWords(original, current);

  return (
    <>
      {tokens.map((token, index) => (
        <span
          key={index}
          className={
            token.type === "added"
              ? "diff-added"
              : token.type === "removed"
              ? "diff-removed"
              : undefined
          }
        >
          {token.text + " "}
        </span>
      ))}
    </>
  );
}
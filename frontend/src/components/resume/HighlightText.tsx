// import type { DiffStatus } from "../../utils/resumeDiff";

// interface Props {
//   text?: string;
//   status: DiffStatus;
//   children: React.ReactNode;
// }

// export default function HighlightText({ status, text, children }: Props) {
//   if (!text) return null;
//   switch (status) {
//     case "added":
//       return (
//         <span
//           className="
//             bg-green-200
//             rounded
//             px-1
//             transition-all
//           "
//         >
//           {children}
//         </span>
//       );

//     case "modified":
//       return (
//         <span
//           className="
//             bg-yellow-200
//             rounded
//             px-1
//             transition-all
//           "
//         >
//           {children}
//         </span>
//       );

//     case "removed":
//       return (
//         <span
//           className="
//             bg-red-200
//             rounded
//             px-1
//             line-through
//             opacity-70
//           "
//         >
//           {children}
//         </span>
//       );

//     default:
//       return <>{children}</>;
//   }
// }

// import type { DiffStatus } from "../../utils/resumeDiff";


// interface Props {
//   text?: string;
//   status: DiffStatus;
// }

// export default function HighlightText({
//   text = "",
//   status,
// }: Props) {
//   const className = {
//     added: "bg-green-200 rounded px-1",
//     modified: "bg-yellow-200 rounded px-1",
//     removed: "bg-red-200 rounded px-1 line-through opacity-70",
//     same: "",
//   }[status];

//   return <span className={className}>{text}</span>;
// }

import { diffWords } from "../../utils/resumeDiff";

interface Props {
  original?: string;
  current?: string;
}

export default function HighlightText({
  original = "",
  current = "",
}: Props) {
  const tokens = diffWords(original, current);

  console.log(tokens);

  return (
    <>
      {tokens.map((token, index) => (
        <span
          key={index}
          style={{
            background:
              token.type === "added"
                ? "lime"
                : token.type === "removed"
                ? "red"
                : "transparent",
            color: token.type === "removed" ? "white" : "black",
            textDecoration:
              token.type === "removed"
                ? "line-through"
                : "none",
          }}
        >
          {token.text + " "}
        </span>
      ))}
    </>
  );
}

// import { diffWords } from "../../utils/resumeDiff";

// interface Props {
//   original?: string;
//   current?: string;
//   showRemoved?: boolean;
// }

// export default function HighlightText({
//   original = "",
//   current = "",
//   showRemoved = false,
// }: Props) {
//   const tokens = diffWords(original, current);

//   return (
//     <>
//       {tokens.map((token, index) => {
//         if (token.type === "removed" && !showRemoved) {
//           return null;
//         }

//         let className = "";

//         switch (token.type) {
//           case "added":
//             className =
//               "bg-green-200 rounded px-1 mx-[1px]";
//             break;

//           case "removed":
//             className =
//               "bg-red-200 line-through opacity-70 rounded px-1 mx-[1px]";
//             break;

//           default:
//             className = "";
//         }

//         return (
//           <span key={index} className={className}>
//             {token.text}{" "}
//           </span>
//         );
//       })}
//     </>
//   );
// }
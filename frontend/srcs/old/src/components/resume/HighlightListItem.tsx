// import HighlightText from "./HighlightText";
// import type { DiffStatus } from "../../utils/resumeDiff";

// interface Props {
//   status: DiffStatus;
//   value: string;
// }

// export default function HighlightListItem({
//   status,
//   value,
// }: Props) {
//   return (
//     <li>
//       <HighlightText status={status}>
//         {value}
//       </HighlightText>
//     </li>
//   );
// }

import HighlightText from "./HighlightText";
import type { DiffStatus } from "../../utils/resumeDiff";

interface Props {
  text: string;
  status: DiffStatus;
}

export default function HighlightListItem({
  text,
  status,
}: Props) {
  return (
    <li>
      <HighlightText text={text} status={status} />
    </li>
  );
}
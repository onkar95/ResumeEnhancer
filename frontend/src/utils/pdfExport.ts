// @ts-ignore -- html2pdf.js ships no bundled TypeScript types
import html2pdf from "html2pdf.js";

export function exportResumeToPdf(elementId: string, filename: string) {
  const element = document.getElementById(elementId);

  if (!element) {
    console.error(`exportResumeToPdf: no element with id="${elementId}"`);
    return;
  }

  console.log("pdfdwnload")
  try {
    html2pdf()
      .set({
        margin: 10,
        filename,
        image: { type: "jpeg", quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: "mm", format: "a4", orientation: "portrait" },
      })
      .from(element)
      .save();
  } catch (error) {
    console.log(error)
  }

}
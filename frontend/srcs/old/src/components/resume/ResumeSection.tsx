import React from "react";

interface Props {
  title: string;
  children: React.ReactNode;
}

export default function ResumeSection({ title, children }: Props) {
  return (
    <section className="mb-6">
      <h2
        className="
    uppercase
    font-bold
    text-sm
    tracking-wider
    border-b-2
    border-gray-300
    pb-1
    mb-3
    "
      >
        {title}
      </h2>

      {children}
    </section>
  );
}

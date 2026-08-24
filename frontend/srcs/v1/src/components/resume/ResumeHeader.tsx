interface Props {
  resume: any;
}

export default function ResumeHeader({ resume }: Props) {
  return (
    <div className="mb-6 text-center">
      {" "}
      <h1 className="text-3xl font-bold">{resume.name} </h1>
     
      <p className="text-gray-600 mt-2">{resume.headline}</p>
      <div className="flex flex-wrap justify-center gap-3 mt-3 text-sm text-gray-500">
        <span>{resume.contact_info?.location}</span>
        <span>{resume.contact_info?.phone}</span>
        <span>{resume.contact_info?.email}</span>
      </div>
    </div>
  );
}

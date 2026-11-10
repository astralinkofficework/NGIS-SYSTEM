import { schoolOverview, listClasses, findProblems, classTimetable } from "@/lib/mcpClient";
import { TimetableView } from "@/components/schedule/TimetableView";
import { notFound } from "next/navigation";

export const dynamic = "force-dynamic";

export default async function SchedulePage({
  params,
}: Readonly<{ params: Promise<{ classId?: string }> }>) {
  const { classId } = await params;
  const [overview, classesResult, problemsResult] = await Promise.all([
    schoolOverview(),
    listClasses(),
    findProblems(),
  ]);

  const classes = classesResult.classes;
  const defaultClass = classId || classes[0]?.id || "7A";
  if (!classes.some((c) => c.id === defaultClass) && classes.length > 0) {
    // allow unknown class ids to still render (server may have data)
  }

  const grid = await classTimetable(defaultClass, 1);

  return (
    <TimetableView
      initialClasses={classes}
      initialProblems={problemsResult.problems}
      initialGrid={grid.grid}
      defaultClass={defaultClass}
      overview={overview.raw}
    />
  );
}

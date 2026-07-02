import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";
import HomepageContent from "@/components/HomepageContent";

const Page = async () => {
  const session = await auth();
  if (!session) {
    redirect("/sign-in");
  }

  return <HomepageContent />;
};

export default Page;

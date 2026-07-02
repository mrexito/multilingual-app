/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { LabeledInput } from "@/components/ui/labeled-input";
import { UserProfile } from "@/lib/user";

type ProfilePageContentProps = {
  userProfile: UserProfile;
};

export default function ProfilePageContent({
  userProfile,
}: ProfilePageContentProps) {
  const router = useRouter();
  const [errors, setErrors] = useState<any>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const validateForm = (formData: FormData) => {
    const newErrors: any = {};

    const email = formData.get("email") as string;
    const password = formData.get("password") as string;
    const confirmPassword = formData.get("confirmPassword") as string;
    const emailPattern = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
    if (!emailPattern.test(email)) {
      newErrors.email = "Please enter a valid email address.";
    }
    if (password && password !== confirmPassword) {
      newErrors.password = "Passwords do not match.";
      newErrors.confirmPassword = "Passwords do not match.";
    }

    return newErrors;
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsSubmitting(true);
    setErrors({});

    const formData = new FormData(e.currentTarget);
    const validationErrors = validateForm(formData);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      setIsSubmitting(false);
      return;
    }
    const res = await fetch("/api/profile", {
      method: "PUT",
      body: formData,
    });
    const data = await res.json();

    if (data.success) {
      router.refresh();
    } else {
      setErrors({
        general: data.error || "An error occurred updating your profile.",
      });
    }
    setIsSubmitting(false);
  };

  return (
    <div className="w-5/6 m-auto">
      <h1 className="text-2xl font-bold mb-2">Your Profile</h1>
      <span className="text-[#ACB1BC]">Update your personal details here</span>

      <form className="space-y-4 mt-6" onSubmit={handleSubmit}>
        <LabeledInput
          label="First Name"
          name="firstname"
          type="text"
          required
          defaultValue={userProfile.firstname || ""}
        />
        <LabeledInput
          label="Last Name"
          name="lastname"
          type="text"
          required
          defaultValue={userProfile.lastname || ""}
        />
        <LabeledInput
          label="Email Address"
          name="email"
          type="email"
          required
          defaultValue={userProfile.email}
          error={errors.email}
        />
        <LabeledInput
          label="Username"
          name="username"
          type="text"
          required
          defaultValue={userProfile.username}
          error={errors.username}
        />
        <LabeledInput
          label="New Password"
          name="password"
          placeholder="Enter new password"
          type="password"
          error={errors.password}
          defaultValue=""
        />
        <LabeledInput
          label="Confirm Password"
          name="confirmPassword"
          placeholder="Repeat new password"
          type="password"
          error={errors.confirmPassword}
          defaultValue=""
        />

        {errors.general && <p className="text-red-600">{errors.general}</p>}

        <Button
          className="w-full mt-12 bg-[#475467] hover:bg-[#2a313c]"
          type="submit"
          disabled={isSubmitting}
        >
          {isSubmitting ? "Updating..." : "Update Profile"}
        </Button>
      </form>
    </div>
  );
}

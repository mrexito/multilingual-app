/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { LabeledInput } from "@/components/ui/labeled-input";
import Link from "next/link";

export default function SignupForm() {
  const router = useRouter();

  const [errors, setErrors] = useState<any>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateForm = (formData: FormData) => {
    const newErrors: any = {};
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;
    const confirmPassword = formData.get("confirmPassword") as string;

    if (password !== confirmPassword) {
      newErrors.password = "Passwords do not match.";
      newErrors.confirmPassword = "Passwords do not match.";
    }

    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailPattern.test(email)) {
      newErrors.email = "Please enter a valid email address.";
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

    const payload = Object.fromEntries(formData.entries());

    const res = await fetch("/api/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (data.success) {
      router.push("/sign-in");
    } else {
      setErrors({
        general: data.error || "An error occurred. Please try again.",
      });
    }

    setIsSubmitting(false);
  };

  return (
    <div className="w-5/6 m-auto">
      <h1 className="text-2xl font-bold mb-2">Enter your Data</h1>
      <span className="text-[#ACB1BC]">
        Complete this step to access the platform
      </span>

      <form className="space-y-4 mt-6" onSubmit={handleSubmit}>
        <LabeledInput
          label="First Name"
          name="firstname"
          placeholder="Max"
          type="text"
          required
          autoComplete="given-name"
          error={errors.firstname}
        />
        <LabeledInput
          label="Last Name"
          name="lastname"
          placeholder="Mustermann"
          type="text"
          required
          autoComplete="family-name"
          error={errors.lastname}
        />
        <LabeledInput
          label="Email Address"
          name="email"
          placeholder="max.mustermann@gmail.com"
          type="email"
          required
          autoComplete="email"
          error={errors.email}
        />
        <LabeledInput
          label="Username"
          name="username"
          placeholder="maxmuster"
          type="text"
          required
          error={errors.username}
        />
        <LabeledInput
          label="Password"
          name="password"
          placeholder="Password"
          type="password"
          required
          autoComplete="new-password"
          error={errors.password}
        />
        <LabeledInput
          label="Confirm Password"
          name="confirmPassword"
          placeholder="Confirm password"
          type="password"
          required
          autoComplete="new-password"
          error={errors.confirmPassword}
        />

        {errors.general && <p className="text-red-600">{errors.general}</p>}

        <Button
          className="w-full bg-[#475467] hover:bg-[#2a313c]"
          type="submit"
          disabled={isSubmitting}
        >
          {isSubmitting ? "Signing Up..." : "Sign Up"}
        </Button>
      </form>

      <div className="text-center mt-4">
        <Button variant="link">
          <Link className="text-[#667085]" href="/sign-in">
            Already have an account?{" "}
            <span className="text-[#344054]">Sign in</span>
          </Link>
        </Button>
      </div>
    </div>
  );
}

import { z } from "zod";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
});

export const userSignupSchema = z.object({
  firstname: z.string().min(1, "First name is required"),
  lastname: z.string().min(1, "Last name is required"),
  email: z.string().email("Must be a valid email"),
  username: z.string().min(3, "Username must have at least 3 characters"),
  password: z.string().min(8, "Password must have at least 8 characters"), // your choice
});

export { schema };

import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function getApiUrl(path: string) {
  const base = process.env.NEXT_PUBLIC_API_BASE || ''
  if (path.startsWith('/')) {
    return `${base}${path}`
  }
  return `${base}/${path}`
}

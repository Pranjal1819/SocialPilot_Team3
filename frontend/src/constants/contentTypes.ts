import { Type, Image, Video, GalleryHorizontal, CircleDot, Clapperboard, LucideIcon } from "lucide-react";
import { ContentType } from "@/types/content";

export interface ContentTypeOption {
  value: ContentType;
  label: string;
  icon: LucideIcon;
}

export const contentTypeOptions: ContentTypeOption[] = [
  { value: "text", label: "Text Post", icon: Type },
  { value: "image", label: "Image", icon: Image },
  { value: "video", label: "Video", icon: Video },
  { value: "carousel", label: "Carousel", icon: GalleryHorizontal },
  { value: "story", label: "Story", icon: CircleDot },
  { value: "reel", label: "Reel", icon: Clapperboard },
];
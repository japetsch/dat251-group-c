<!-- A simple preset for buttons -->
<script lang="ts">
    import type { Snippet } from "svelte";

    type Variant = "primary" | "secondary";

    let { variant = "primary", class: className = "", children, onclick}: {
        variant?: Variant;
        class?: string;
        children?: Snippet;
        onclick?: (event: MouseEvent) => void;
    } = $props();

    const base = "inline-flex items-center justify-center rounded-full px-6 py-3 text-base font-medium transition shadow-sm";

    const variants = {
        primary: "border border-black/10 bg-red-600 text-white hover:bg-red-700",
        secondary: "border border-black/10 bg-[#e6dfdd] text-black hover:bg-[#ddd5d3]"
    };
</script>

<button class={`${base} ${variants[variant]} ${className}`} {onclick}>
    {@render children?.()}
</button>
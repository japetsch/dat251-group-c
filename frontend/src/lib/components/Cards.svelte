<!-- A simple preset for cards -->
<script lang="ts">
    import type { Snippet } from "svelte";

    type Orientation = "vertical" | "horizontal";
    type Tone = "white" | "red";

    let { title = "", orientation = "vertical", tone = "white", class: className = "", children}: {
        title?: String;
        orientation?: Orientation;
        tone?: Tone;
        class?: string;
        children?: Snippet;
    } = $props();

    const base = "rounded-[22px] px-6 py-6 shadow-sm border";

    const orientationClasses = {
        vertical: "w-full max-w-[360px]",
        horizontal: "w-full max-w-[760px]"
    };

    const toneClasses = {
        white: "border-black/10 bg-white text-black",
        red: "border-red-200 bg-red-50 text-red-950"
    };

    const titleClasses = {
        white: "text-black",
        red: "text-red-900"
    };

    const bodyClasses ={
        white: "text-black/75",
        red: "text-red-950/80"
    };
</script>

<div class={`${base} ${orientationClasses[orientation]} ${toneClasses[tone]} ${className}`}>
    {#if title}
        <h3 class={`mb-4 text-xl font-semibold tracking-tight ${titleClasses[tone]}`}>
            {title}
        </h3>
    {/if}

    <div class={`text-base leading-6 ${bodyClasses[tone]}`}>
        {@render children?.()}
    </div>
</div>
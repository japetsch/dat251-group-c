<script lang="ts">
  import Buttons from "$lib/components/Buttons.svelte";
  import Cards from "$lib/components/Cards.svelte";
  import { Button } from "$lib/components/ui/button";
  import { onMount } from "svelte";
  import "../app.css";

  // variables for the display of bloodbanks
  type Bloodbank = {
    bloodbank_id: number;
    name: string;
    street_name: string;
    street_number: string;
    postal_code: string;
    city: string;
    country: string;
    user_has_admin_access: boolean;
  };

  let bloodbanks = $state<Bloodbank[]>([]);
  let bloodbanksLoading = $state(true);
  let bloodbanksError = $state<string | null>(null);

  onMount(async () => {
    try {
      const response = await fetch("/api/bloodbank");

      if (!response.ok) {
        bloodbanksError = "Kunne ikke hente blodbanker.";
        return;
      }
      bloodbanks = await response.json();
    } catch {
      bloodbanksError = "Kunne ikke hente blodbanker.";
    } finally {
      bloodbanksLoading = false;
    }
  });

  // variables for the questionnaire
  let showEligibility = $state(false);

  let ageOk = $state<boolean | null>(null);
  let weightOk = $state<boolean | null>(null);
  let healthyOk = $state<boolean | null>(null);
  let recentDonationOk = $state<boolean | null>(null);
  let idOk = $state<boolean | null>(null);

  const allAnswered = $derived(
    ageOk !== null &&
      weightOk !== null &&
      healthyOk !== null &&
      recentDonationOk !== null &&
      idOk !== null,
  );

  const eligible = $derived(
    ageOk === true &&
      weightOk === true &&
      healthyOk === true &&
      recentDonationOk === true &&
      idOk === true,
  );

  function resetEligibility() {
    ageOk = null;
    weightOk = null;
    healthyOk = null;
    recentDonationOk = null;
    idOk = null;
  }

  //contents of the cards for the info section
  const stats = [
    { value: "3", label: "Liv reddet per donasjon" },
    { value: "5%", label: "Av befolkningen som donerer" },
    { value: "45 min", label: "Gjennomsnittlig donasjonstid" },
  ];

  const donorRequirements = [
    "Være mellom 18 og 70 år",
    "Veie minst 50kg",
    "Være ved god helse",
    "Ikke nylig donert blod",
  ];

  const donationSteps = [
    "Registrering og helsesjekk",
    "Blodprøve for å sjekke hemoglobin",
    "Selve donasjonen",
    "Hvile og noe å spise etterpå",
  ];

  //function for scrolling the info section into view
  const scrollToInfo = () => {
    const section = document.getElementById("info-section");
    section?.scrollIntoView({ behavior: "smooth" });
  };
</script>

<!-- The first page -->
<div class="min-h-screen bg-[#f5f2f1] text-black">
  <section
    class="relative flex min-h-screen items-center justify-center overflow-hidden"
  >
    <div
      class="absolute inset-0 bg-cover bg-bottom bg-no-repeat opacity-100"
      style="background-image: url('/Background_Bloodbank.png');"
    ></div>

    <!-- The login button routed to /login -->
    <a href="/login">
      <div class="fixed right-6 top-6 z-50">
        <Buttons variant="primary">Logg inn</Buttons>
      </div>
    </a>

    <!-- Formating of the contents inside the card -->
    <div
      class="relative z-10 inline-block rounded-[32px] border border-black/10 bg-white px-[7rem] py-[4rem] text-center shadow-[0_4px_18px_rgba(0,0,0,0.05)]"
    >
      <div class="flex flex-col items-center gap-14">
        <img
          src="/tmp_logo.svg"
          alt="Norges Blodbank logo"
          class="mx-auto h-40 w-40"
        />

        <h1 class="text-8xl font-semibold tracking-tight">Norges Blodbank</h1>
        <p class="text-4xl text-black/70">
          Bestill time for blodgiving ved blodbanker i hele Norge.
        </p>

        <div class="mt-8 flex justify-center gap-6">
          <Buttons
            variant="primary"
            class="px-12 py-8 !text-3xl"
            onclick={() => (showEligibility = true)}
            >Sjekk om du kan donere</Buttons
          >
          <Buttons
            variant="secondary"
            class="px-12 py-8 !text-3xl"
            onclick={scrollToInfo}>Les mer</Buttons
          >
        </div>
      </div>
    </div>
  </section>

  <!-- The info page -->
  <section id="info-section" class="min-h-screen px-6 py-12 flex items-center">
    <div class="mx-auto max-w-6xl space-y-12">
      <div class="space-y-4 text-center">
        <h2 class="text-4xl font-semibold tracking-tight">Hvorfor gi blod?</h2>
        <p class="mx-auto max-w-3xl text-lg leading-8 text-black/65">
          Bloddonasjon er en av de viktigste måtene du kan hjelpe andre på. Hvor
          donasjon kan redde opptil tre liv.
        </p>
      </div>

      <div class="flex flex-wrap justify-center gap-6">
        {#each stats as stat}
          <Cards orientation="vertical" tone="white" class="text-center">
            <div class="text-4xl font-semibold tracking-tight">
              {stat.value}
            </div>
            <p class="mt-3">{stat.label}</p>
          </Cards>
        {/each}
      </div>

      <div class="flex flex-wrap justify-center gap-6">
        <Cards title="Hvem kan donere?" orientation="vertical" tone="white">
          <ul class="space-y-2">
            {#each donorRequirements as item}
              <li>{item}</li>
            {/each}
          </ul>
        </Cards>

        <Cards
          title="Hva skjer under donasjonen?"
          orientation="vertical"
          tone="white"
        >
          <ul class="space-y-2">
            {#each donationSteps as item}
              <li>{item}</li>
            {/each}
          </ul>
        </Cards>
      </div>

      <div class="flex justify-center">
        <Cards title="Trygt og sikkert" orientation="horizontal" tone="red">
          <p>
            Alle donasjoner gjennomføres med sterilt engangsutstyr, og du blir
            fulgt opp av helsepersonell gjennom hele prosessen.
          </p>
        </Cards>
      </div>
    </div>
  </section>

  <!-- Display bloodbanks -->
  <section class="min-h-screen bg-[#f5f2f1] px-6 py-12 flex items-center">
    <div class="mx-auto w-full max-w-5xl space-y-8">
      <div class="space-y-3 text-center">
        <h2 class="text-3xl font-semibold tracking-tight">Finn en blodbank</h2>
        <p class="mx-auto max-w-3xl text-base leading-7 text-black/65">
          Her er blodbanker du kan bestille time hos.
        </p>
      </div>

      {#if bloodbanksLoading}
        <p class="text-center text-black/65">Laster blodbanker...</p>
      {:else if bloodbanksError}
        <p class="text-center text-red-700">{bloodbanksError}</p>
      {:else if bloodbanks.length === 0}
        <p class="text-center text-black/65">Ingen blodbanker funnet.</p>
      {:else}
        <div class="flex flex-wrap justify-center gap-6">
          {#each bloodbanks as bloodbank}
            <Cards
              orientation="vertical"
              tone="white"
              class="w-full max-w-[360px]"
            >
              <div class="space-y-2">
                <h3 class="text-xl font-semibold tracking-tight">
                  {bloodbank.name}
                </h3>
                <p class="text-black/70">
                  {bloodbank.street_name}
                  {bloodbank.street_number}
                </p>
                <p class="text-black/70">
                  {bloodbank.postal_code}
                  {bloodbank.city}
                </p>
                <p class="text-black/70">{bloodbank.country}</p>
              </div>
            </Cards>
          {/each}
        </div>
      {/if}
    </div>
  </section>

  <!-- Handling of the questionnaire -->
  {#if showEligibility}
    <Button
      type="button"
      class="fixed"
      aria-label="Lukk donor-sjekk"
      onclick={() => (showEligibility = false)}
    ></Button>
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <Cards orientation="horizontal" tone="white" class="w-full max-w-[44rem]">
        <div class="space-y-3">
          <div class="flex items-start justify-between gap-4">
            <div>
              <h2 class="text-xl font-semibold tracking-tight">
                Sjekk om du kan donere blod
              </h2>
              <p class="mt-1 text-black/70">
                Dette er en enkel veiledning og erstatter ikke vurdering fra
                blodbanken.
              </p>
            </div>
            <Buttons
              variant="secondary"
              onclick={() => (showEligibility = false)}>Lukk</Buttons
            >
          </div>
          <div class="space-y-4">
            <div
              class="rounded-[18px] border border-black/10 bg-[#faf7f6] px-4 py-4"
            >
              <p class="mb-3 text-lg font-medium">Er du mellom 18 og 70 år?</p>
              <div class="flex gap-3">
                <Button
                  type="button"
                  class={`rounded-full border px-5 py-2.5 text-sm font-medium transition ${
                    ageOk === true
                      ? "border-black/15 bg-[#d9d2cf] text-black hover:bg-[#f3eeed]"
                      : "border-black/10 bg-white text-black hover:bg-[#f3eeed]"
                  }`}
                  onclick={() => (ageOk = true)}
                >
                  Ja
                </Button>
                <Button
                  type="button"
                  class={`rounded-full border px-5 py-2.5 text-sm font-medium transition ${
                    ageOk === false
                      ? "border-black/15 bg-[#d9d2cf] text-black hover:bg-[#f3eeed]"
                      : "border-black/10 bg-white text-black hover:bg-[#f3eeed]"
                  }`}
                  onclick={() => (ageOk = false)}
                >
                  Nei
                </Button>
              </div>
            </div>

            <div
              class="rounded-[18px] border border-black/10 bg-[#faf7f6] px-4 py-4"
            >
              <p class="mb-3 text-lg font-medium">Veier du minst 50 kg?</p>
              <div class="flex gap-3">
                <Button
                  type="button"
                  class={`rounded-full border px-5 py-2.5 text-sm font-medium transition ${
                    weightOk === true
                      ? "border-black/15 bg-[#d9d2cf] text-black hover:bg-[#f3eeed]"
                      : "border-black/10 bg-white text-black hover:bg-[#f3eeed]"
                  }`}
                  onclick={() => (weightOk = true)}
                >
                  Ja
                </Button>
                <Button
                  type="button"
                  class={`rounded-full border px-5 py-2.5 text-sm font-medium transition ${
                    weightOk === false
                      ? "border-black/15 bg-[#d9d2cf] text-black hover:bg-[#f3eeed]"
                      : "border-black/10 bg-white text-black hover:bg-[#f3eeed]"
                  }`}
                  onclick={() => (weightOk = false)}
                >
                  Nei
                </Button>
              </div>
            </div>

            <div
              class="rounded-[18px] border border-black/10 bg-[#faf7f6] px-4 py-4"
            >
              <p class="mb-3 text-lg font-medium">
                Føler du deg frisk og i god helse i dag?
              </p>
              <div class="flex gap-3">
                <Button
                  type="button"
                  class={`rounded-full border px-5 py-2.5 text-sm font-medium transition ${
                    healthyOk === true
                      ? "border-black/15 bg-[#d9d2cf] text-black hover:bg-[#f3eeed]"
                      : "border-black/10 bg-white text-black hover:bg-[#f3eeed]"
                  }`}
                  onclick={() => (healthyOk = true)}
                >
                  Ja
                </Button>
                <Button
                  type="button"
                  class={`rounded-full border px-5 py-2.5 text-sm font-medium transition ${
                    healthyOk === false
                      ? "border-black/15 bg-[#d9d2cf] text-black hover:bg-[#f3eeed]"
                      : "border-black/10 bg-white text-black hover:bg-[#f3eeed]"
                  }`}
                  onclick={() => (healthyOk = false)}
                >
                  Nei
                </Button>
              </div>
            </div>

            <div
              class="rounded-[18px] border border-black/10 bg-[#faf7f6] px-4 py-4"
            >
              <p class="mb-3 text-lg font-medium">
                Har det gått lenge nok siden sist du donerte blod?
              </p>
              <div class="flex gap-3">
                <Button
                  type="button"
                  class={`rounded-full border px-5 py-2.5 text-sm font-medium transition ${
                    recentDonationOk === true
                      ? "border-black/15 bg-[#d9d2cf] text-black hover:bg-[#f3eeed]"
                      : "border-black/10 bg-white text-black hover:bg-[#f3eeed]"
                  }`}
                  onclick={() => (recentDonationOk = true)}
                >
                  Ja
                </Button>
                <Button
                  type="button"
                  class={`rounded-full border px-5 py-2.5 text-sm font-medium transition ${
                    recentDonationOk === false
                      ? "border-black/15 bg-[#d9d2cf] text-black hover:bg-[#f3eeed]"
                      : "border-black/10 bg-white text-black hover:bg-[#f3eeed]"
                  }`}
                  onclick={() => (recentDonationOk = false)}
                >
                  Nei
                </Button>
              </div>
            </div>

            <div
              class="rounded-[18px] border border-black/10 bg-[#faf7f6] px-4 py-4"
            >
              <p class="mb-3 text-lg font-medium">Har du norsk personnummer?</p>
              <div class="flex gap-3">
                <Button
                  type="button"
                  class={`rounded-full border px-5 py-2.5 text-sm font-medium transition ${
                    idOk === true
                      ? "border-black/15 bg-[#d9d2cf] text-black hover:bg-[#f3eeed]"
                      : "border-black/10 bg-white text-black hover:bg-[#f3eeed]"
                  }`}
                  onclick={() => (idOk = true)}
                >
                  Ja
                </Button>
                <Button
                  type="button"
                  class={`rounded-full border px-5 py-2.5 text-sm font-medium transition ${
                    idOk === false
                      ? "border-black/15 bg-[#d9d2cf] text-black hover:bg-[#f3eeed]"
                      : "border-black/10 bg-white text-black hover:bg-[#f3eeed]"
                  }`}
                  onclick={() => (idOk = false)}
                >
                  Nei
                </Button>
              </div>
            </div>
          </div>

          {#if allAnswered}
            <div
              class={`rounded-[20px] border p-5 ${eligible ? "border-green-200 bg-green-50" : "border-red-200 bg-red-50"}`}
            >
              {#if eligible}
                <p class="mb-3 text-lg font-medium">
                  Du kan sannsynligvis donere blod.
                </p>
                <p class="mt-2 text-black/70">
                  Neste steg er å bestille time eller kontakte blodbanken for
                  endelig vurdering.
                </p>
              {:else}
                <p class="mb-3 text-lg font-medium">
                  Du bør kontakte blodbanken før du bestiller time.
                </p>
                <p class="mt-2 text-black/70">
                  Ett ellere flere svar tyder på at du kanskje ikke kan donere
                  blod akkurat nå.
                </p>
              {/if}
            </div>
          {/if}

          <div class="flex justify-end">
            <Buttons variant="secondary" onclick={resetEligibility}
              >Nullstill</Buttons
            >
          </div>
        </div>
      </Cards>
    </div>
  {/if}
</div>

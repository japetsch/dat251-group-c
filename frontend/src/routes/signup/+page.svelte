<style>
  .page {
    min-height: 100vh;
    background: #f5f2f1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 3rem 2rem;
  }

  .panel-right {
    width: 100%;
  }

  form {
    width: 100%;
    max-width: 780px;
    margin: 0 auto;
    background: white;
    border-radius: 1.5rem;
    border: 1px solid rgba(0, 0, 0, 0.08);
    padding: 3rem 3.5rem;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.05);
  }

  h2 {
    font-size: 1.7rem;
    font-weight: 700;
    color: black;
    margin-bottom: 2rem;
  }

  .section-title {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: rgba(0, 0, 0, 0.4);
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
    padding-bottom: 0.4rem;
  }

  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.9rem;
  }

  label {
    display: flex;
    flex-direction: column;
    font-size: 0.875rem;
    font-weight: 600;
    color: black;
    gap: 0.35rem;
  }

  .optional {
    font-weight: 400;
    color: rgba(0, 0, 0, 0.4);
  }

  input,
  select {
    padding: 0.7rem 0.9rem;
    border-radius: 0.6rem;
    border: 1px solid rgba(0, 0, 0, 0.1);
    font-size: 0.95rem;
    background: #faf7f6;
    transition: border-color 0.15s;
  }

  input:focus,
  select:focus {
    outline: none;
    border-color: rgba(0, 0, 0, 0.3);
  }

  .error {
    color: #dc2626;
    font-size: 0.875rem;
    font-weight: 600;
    margin-top: 0.75rem;
  }

  button {
    margin-top: 1.5rem;
    width: 100%;
    padding: 0.9rem;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 999px;
    background: #dc2626;
    color: white;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.15s;
  }

  button:hover {
    background: #b91c1c;
  }
</style>

<script lang="ts">
  import { onMount } from "svelte";

  let name = "";
  let email = "";
  let phone = "";
  let password = "";
  let streetName = "";
  let streetNumber = "";
  let aptNumber = "";
  let postalCode = "";
  let city = "";
  let country = "";
  let bloodType = "";
  let preferredBloodbankId: number | null = null;
  let error = "";

  let bloodbanks: { bloodbank_id: number; name: string }[] = [];

  onMount(async () => {
    const res = await fetch("/api/bloodbank");
    if (res.ok) {
      bloodbanks = await res.json();
      if (bloodbanks.length > 0) {
        preferredBloodbankId = bloodbanks[0].bloodbank_id;
      }
    }
  });

  async function submitSignup(event: SubmitEvent) {
    event.preventDefault();
    error = "";

    const signupRes = await fetch("/api/auth/signup-donor", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        email,
        password,
        phone_number: phone,
        street_name: streetName,
        street_number: streetNumber,
        apt_number: aptNumber || null,
        postal_code: postalCode,
        city,
        country,
        blood_type: bloodType || null,
        preferred_bloodbank_id: preferredBloodbankId,
      }),
    });

    if (!signupRes.ok) {
      if (signupRes.status === 400) {
        error = "E-postadressen er allerede i bruk, eller dataene er ugyldige.";
      } else if (signupRes.status === 422) {
        let data: any = null;
        try {
          data = await signupRes.json();
        } catch {
          data = null;
        }
        error =
          data?.detail?.[0]?.msg ||
          "Ugyldig data – sjekk at alle felt er fylt ut riktig.";
      } else {
        error = "Noe gikk galt. Prøv igjen.";
      }
      return;
    }

    window.location.href = "/login?registrert=1";
  }
</script>

<a href="/" class="fixed left-6 top-6 z-50 transition hover:opacity-80">
  <img src="/tmp_logo.svg" alt="Til forsiden" class="h-20 w-20" />
</a>

<div class="page">
  <div class="panel-right">
    <form onsubmit={submitSignup}>
      <h2>Opprett konto</h2>

      <div class="section-title">Personalia</div>
      <div class="grid-2">
        <label>
          Navn
          <input bind:value={name} required placeholder="Ola Nordmann" />
        </label>
        <label>
          E-post
          <input
            type="email"
            bind:value={email}
            required
            placeholder="ola@example.com"
          />
        </label>
        <label>
          Telefonnummer
          <input bind:value={phone} required placeholder="12345678" />
        </label>
        <label>
          Passord
          <input
            type="password"
            bind:value={password}
            required
            placeholder="••••••••"
          />
        </label>
      </div>

      <div class="section-title">Adresse</div>
      <div class="grid-2">
        <label class="span-2-on-small">
          Gatenavn
          <input bind:value={streetName} required placeholder="Storgaten" />
        </label>
        <label>
          Gatenummer
          <input bind:value={streetNumber} required placeholder="1" />
        </label>
        <label>
          <span>Leilighetsnummer <span class="optional">(valgfritt)</span></span
          >
          <input bind:value={aptNumber} placeholder="H0101" />
        </label>
        <label>
          Postnummer
          <input bind:value={postalCode} required placeholder="5000" />
        </label>
        <label>
          By
          <input bind:value={city} required placeholder="Bergen" />
        </label>
        <label>
          Land
          <input bind:value={country} required placeholder="Norge" />
        </label>
      </div>

      <div class="section-title">Donasjon</div>
      <div class="grid-2">
        <label>
          <span>Blodtype <span class="optional">(valgfritt)</span></span>
          <select bind:value={bloodType}>
            <option value="">Ukjent</option>
            <option value="A+">A+</option>
            <option value="A-">A-</option>
            <option value="B+">B+</option>
            <option value="B-">B-</option>
            <option value="AB+">AB+</option>
            <option value="AB-">AB-</option>
            <option value="O+">O+</option>
            <option value="O-">O-</option>
          </select>
        </label>
        <label>
          Foretrukket blodbank
          <select bind:value={preferredBloodbankId} required>
            {#each bloodbanks as bb}
              <option value={bb.bloodbank_id}>{bb.name}</option>
            {/each}
          </select>
        </label>
      </div>

      {#if error}
        <p class="error">{error}</p>
      {/if}

      <button type="submit">Registrer deg</button>
    </form>
  </div>
</div>

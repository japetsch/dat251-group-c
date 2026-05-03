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
  let success = "";

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
    success = "";

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
      let data: any = null;
      try {
        data = await signupRes.json();
      } catch {
        data = null;
      }
      error =
        data?.detail?.[0]?.msg ||
        data?.detail ||
        data?.message ||
        "Kunne ikke registrere bruker.";
      return;
    }

    const loginRes = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (loginRes.ok) {
      window.location.href = "/appointment/list";
    } else {
      window.location.href = "/login";
    }
  }
</script>

<section class="signup-page">
  <div class="card">
    <h1>Registrer deg som blodgiver</h1>
    <p>Fyll inn informasjonen din for å opprette en bruker.</p>

    <form onsubmit={submitSignup}>
      <label>
        Navn
        <input bind:value={name} required />
      </label>

      <label>
        E-post
        <input type="email" bind:value={email} required />
      </label>

      <label>
        Telefonnummer
        <input bind:value={phone} required />
      </label>

      <label>
        Passord
        <input type="password" bind:value={password} required />
      </label>

      <label>
        Gatenavn
        <input bind:value={streetName} required />
      </label>

      <label>
        Gatenummer
        <input bind:value={streetNumber} required />
      </label>

      <label>
        Leilighetsnummer (valgfritt)
        <input bind:value={aptNumber} />
      </label>

      <label>
        Postnummer
        <input bind:value={postalCode} required />
      </label>

      <label>
        By
        <input bind:value={city} required />
      </label>

      <label>
        Land
        <input bind:value={country} required />
      </label>

      <label>
        Blodtype
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

      {#if error}
        <p class="error">{error}</p>
      {/if}

      {#if success}
        <p class="success">{success}</p>
      {/if}

      <button type="submit">Registrer deg</button>
    </form>
  </div>
</section>

<style>
  .signup-page {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #fff3f5;
    padding: 2rem;
  }

  .card {
    background: white;
    padding: 3rem;
    border-radius: 2rem;
    width: 100%;
    max-width: 520px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
  }

  h1 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
  }

  p {
    color: #444;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 2rem;
  }

  label {
    display: flex;
    flex-direction: column;
    font-weight: 600;
    gap: 0.4rem;
  }

  input,
  select {
    padding: 0.9rem;
    border-radius: 0.8rem;
    border: 1px solid #ccc;
    font-size: 1rem;
  }

  button {
    margin-top: 1rem;
    padding: 1rem;
    border: none;
    border-radius: 999px;
    background: #e60000;
    color: white;
    font-weight: 700;
    font-size: 1rem;
    cursor: pointer;
  }

  .error {
    color: #c40000;
    font-weight: 600;
  }

  .success {
    color: #067a2f;
    font-weight: 600;
  }
</style>

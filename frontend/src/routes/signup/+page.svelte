<script lang="ts">
  let name = "";
  let email = "";
  let phone = "";
  let birthDate = "";
  let bloodType = "";
  let password = "";
  let error = "";
  let success = "";

  async function submitSignup(event: SubmitEvent) {
    event.preventDefault();

    error = "";
    success = "";

    const response = await fetch("/api/users", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        email,
        phone,
        birth_date: birthDate,
        blood_type: bloodType || null,
        password,
      }),
    });

    let data: any = null;

    try {
      data = await response.json();
    } catch {
      data = null;
    }

    if (!response.ok) {
      console.log("Registrering feilet:", data);
      error =
        data?.detail?.[0]?.msg ||
        data?.detail ||
        data?.message ||
        "Kunne ikke registrere bruker.";
      return;
    }

    success = "Brukeren ble registrert!";
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
        Fødselsdato
        <input type="date" bind:value={birthDate} required />
      </label>

      <label>
        Blodtype
        <select bind:value={bloodType}>
          <option value="">Ukjent</option>
          <option value="A_POS">A+</option>
          <option value="A_NEG">A-</option>
          <option value="B_POS">B+</option>
          <option value="B_NEG">B-</option>
          <option value="AB_POS">AB+</option>
          <option value="AB_NEG">AB-</option>
          <option value="O_POS">O+</option>
          <option value="O_NEG">O-</option>
        </select>
      </label>

      <label>
        Passord
        <input type="password" bind:value={password} required />
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
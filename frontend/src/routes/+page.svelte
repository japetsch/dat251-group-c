<style>
  :global(html) {
    scroll-behavior: smooth;
  }

  :global(body) {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #f8fafc;
    color: #1e293b;
  }

  .hero {
    min-height: 100vh;
    display: grid;
    place-items: center;
    padding: 2rem;
    background: linear-gradient(to bottom right, #f8fafc, #fa0000);
  }

  .login-btn {
    position: fixed;
    top: 2rem;
    right: 2rem;
    text-decoration: none;
    background: white;
    color: #1e293b;
    padding: 0.8rem 1.3rem;
    border-radius: 999px;
    font-weight: 600;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
    transition: 0.2s ease;
    cursor: pointer;
  }

  .login-btn:hover {
    transform: translateY(-2px);
  }

  .container {
    width: 100%;
    max-width: 420px;
    text-align: center;
    background: white;
    padding: 3.5rem 2.5rem;
    border-radius: 2rem;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
  }

  .logo {
    display: flex;
    justify-content: center;
    margin-bottom: 0 0 0.5rem 0;
  }

  /* makeshift logo */
  .drop {
    width: 34px;
    height: 34px;
    background: #ef4444;
    border-radius: 50% 50% 50% 0;
    transform: rotate(-225deg);
    box-shadow: 0 4px 10px rgba(99, 99, 99, 0.35);
  }

  h1 {
    margin: 0;
    font-size: 2.5rem;
    line-height: 1.1;
  }

  .subtitle {
    margin: 0;
    font-size: 1rem;
  }

  .scroll-btn {
    margin-top: 0.5rem;
    border: none;
    background: #e5e7eb;
    color: #1e293b;
    padding: 0.95rem 1.6rem;
    border-radius: 999px;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition:
      background 0.2s ease,
      transform 0.2s ease;
    text-decoration: none;
  }

  .scroll-btn:hover {
    background: #d1d5db;
    transform: translateY(-1px);
  }

  /* Login popup */
  .overlay {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
  }

  .modal {
    position: relative;
    width: min(100%, 640px);
    background: white;
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
  }

  h2 {
    margin: 0;
    font-size: 2rem;
    color: #111827;
  }

  .modal-subtitle {
    margin: 0.75rem 0 1.5rem;
    color: #6b7280;
    font-size: 1.1rem;
  }

  .bankid-btn {
    width: 100%;
    border: none;
    border-radius: 0.75rem;
    background: #2563eb;
    color: white;
    font-size: 1.4rem;
    font-weight: 700;
    padding: 1.25rem;
    cursor: pointer;
    display: block;
    text-align: center;
    margin-bottom: 1rem;
    text-decoration: none;
    box-sizing: border-box;
  }

  .info-box {
    background: #eef2f7;
    border: 1px solid #cfe0f5;
    color: #4b5563;
    border-radius: 0.75rem;
    padding: 1rem;
    font-size: 1rem;
    line-height: 1.5;
  }

  .info-section {
    min-height: 100vh;
    background: #f8f4f4;
    padding: 5rem 2rem;
  }

  .info-content {
    max-width: 1000px;
    margin: 0 auto;
  }

  .info-content h2 {
    margin: 0;
    text-align: center;
    font-size: 2.5rem;
    color: #111827;
  }

  .info-intro {
    max-width: 700px;
    margin: 1rem auto 3rem;
    text-align: center;
    font-size: 1rem;
    line-height: 1.7;
    color: #6b7280;
  }

  .stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .stat-card {
    background: white;
    border-radius: 1rem;
    padding: 2rem 1.5rem;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
  }

  .stat-card h3 {
    margin: 0 0 0.5rem;
    font-size: 2rem;
    color: #111827;
  }

  .stat-card p {
    margin: 0;
    color: #6b7280;
  }

  .info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .info-card {
    background: white;
    border-radius: 1rem;
    padding: 1.75rem;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
  }

  .info-card h3 {
    margin-top: 0;
    margin-bottom: 1rem;
    color: #111827;
  }

  .info-card ul {
    margin: 0;
    padding-left: 1.2rem;
    color: #4b5563;
    line-height: 1.8;
  }

  .safety-box {
    background: #eef4ff;
    border: 1px solid #cfe0ff;
    border-radius: 1rem;
    padding: 1.75rem;
  }

  .safety-box h3 {
    margin-top: 0;
    margin-bottom: 0.75rem;
    color: #111827;
  }

  .safety-box p {
    margin: 0;
    color: #4b5563;
    line-height: 1.7;
  }

  @media (max-width: 800px) {
    .stats,
    .info-grid {
      grid-template-columns: 1fr;
    }
  }

  .info-content h2 {
    font-size: 2rem;
  }
</style>

<script lang="ts">
  import favicon from "$lib/assets/favicon.svg";

  let showLogin = false;

  const title = "Blodbanken";
  const subtitle = "Doner blod. Redd liv.";

  function openLogin() {
    showLogin = true;
  }

  function closeLogin() {
    showLogin = false;
  }

  function handleOverlayClick(e: MouseEvent) {
    if (e.target === e.currentTarget) {
      closeLogin();
    }
  }
</script>

<svelte:head>
  <title>Blodbanken</title>
  <link rel="icon" href={favicon} />
</svelte:head>

<section class="hero">
  <button class="login-btn" onclick={openLogin}>Logg inn</button>

  <div class="container">
    <div class="logo">
      <div class="drop"></div>
    </div>

    <h1>{title}</h1>
    <p class="subtitle">{subtitle}</p>

    <a href="#info-section" class="scroll-btn">Les mer</a>
  </div>

  {#if showLogin}
    <div
      class="overlay"
      role="button"
      tabindex="0"
      onclick={handleOverlayClick}
      onkeydown={(e: KeyboardEvent) => {
        if (e.key === "Enter" || e.key === " ") closeLogin();
        if (e.key === "Escape") closeLogin();
      }}
    >
      <div class="modal" role="dialog" aria-modal="true" tabindex="-1">
        <h2>Logg inn</h2>
        <p class="modal-subtitle">Bruk BankID for sikker pålogging</p>

        <a href="/dashboard" class="bankid-btn">Logg inn med BankID</a>
        <div class="info-box">
          Du vil bli bedt om å identifisere deg med BankID. Dette sikrer at dine
          helseopplysninger forblir trygge og konfidensielle.
        </div>
      </div>
    </div>
  {/if}
</section>

<section id="info-section" class="info-section">
  <div class="info-content">
    <h2>Hvorfor gi blod?</h2>
    <p class="info-intro">
      Bloddonasjon er en av de viktigste måtene du kan hjelpe andre på. Hver
      donasjon kan redde opptil tre liv.
    </p>

    <div class="stats">
      <div class="stat-card">
        <h3>3</h3>
        <p>Liv reddet per donasjon</p>
      </div>

      <div class="stat-card">
        <h3>5%</h3>
        <p>Av befolkningen som donerer</p>
      </div>

      <div class="stat-card">
        <h3>45 min</h3>
        <p>Gjennomsnittlig donasjonstid</p>
      </div>
    </div>

    <div class="info-grid">
      <div class="info-card">
        <h3>Hvem kan donere?</h3>
        <ul>
          <li>Være mellom 18 og 70 år</li>
          <li>Veie minst 50 kg</li>
          <li>Være ved god helse</li>
          <li>Ikke nylig donert blod</li>
        </ul>
      </div>

      <div class="info-card">
        <h3>Hva skjer under donasjonen?</h3>
        <ul>
          <li>Registrering og helsesjekk</li>
          <li>Blodprøve for å sjekke hemoglobin</li>
          <li>Selve donasjonen</li>
          <li>Hvile og noe å spise etterpå</li>
        </ul>
      </div>
    </div>

    <div class="safety-box">
      <h3>Trygt og sikkert</h3>
      <p>
        Alle donasjoner gjennomføres med sterilt engangsutstyr, og du blir fulgt
        opp av helsepersonell gjennom hele prosessen.
      </p>
    </div>
  </div>
</section>

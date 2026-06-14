(() => {
  const INTRO_TIMEOUT_MS = 17000;
  const POLL_MS = 250;
  const startedAt = Date.now();

  function getLoginCard() {
    return document.querySelector('.login-card');
  }

  function getIntro() {
    return document.getElementById('gfieldIntro');
  }

  function getPage2() {
    return document.getElementById('page2');
  }

  function ensureBrief() {
    const login = getLoginCard();
    if (!login) return null;

    let brief = document.getElementById('preLoginBriefRecovery');
    if (brief) return brief;

    brief = document.createElement('section');
    brief.id = 'preLoginBriefRecovery';
    brief.className = 'pre-login-brief';
    brief.innerHTML =
      '<div style="padding:32px 24px">' +
        '<div class="eyebrow">PREMIER HYPER FOCUS</div>' +
        '<h2 style="margin:0 0 12px">프리미어 합격 체크리스트</h2>' +
        '<p>54개 핵심 유형과 회차별 진단 리포트로 프리미어 준비 상태를 먼저 점검합니다.</p>' +
        '<div class="pre-login-grid">' +
          '<div><b>1. 대표 유형 점검</b><span>핵심 사고력 유형을 빠르게 확인합니다.</span></div>' +
          '<div><b>2. 약점 흐름 확인</b><span>회차별 변화와 흔들리는 유형을 봅니다.</span></div>' +
          '<div><b>3. 보완 방향 안내</b><span>다음 학습 포인트를 리포트로 확인합니다.</span></div>' +
        '</div>' +
        '<div style="display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));margin-top:18px">' +
          '<a href="https://naver.me/xy7bsjyb" target="_blank" rel="noopener" style="display:flex;align-items:center;justify-content:center;text-decoration:none;border-radius:14px;padding:17px 18px;font-size:18px;font-weight:900;background:linear-gradient(135deg,#d4af37,#f8dd83);color:#07111e">프로그램 상담 신청하기</a>' +
          '<button type="button" id="preLoginRecoveryStart" style="border:1px solid rgba(248,221,131,.35);border-radius:14px;padding:17px 18px;font-size:18px;font-weight:900;background:rgba(255,255,255,.06);color:#fff;cursor:pointer">로그인해서 진단 시작하기</button>' +
        '</div>' +
      '</div>';

    login.parentNode.insertBefore(brief, login);
    brief.querySelector('#preLoginRecoveryStart').addEventListener('click', () => {
      window.gfieldPreLoginStarted = true;
      brief.style.display = 'none';
      login.classList.remove('prelogin-locked');
      login.style.display = '';
      login.hidden = false;
      login.scrollIntoView({ behavior: 'smooth', block: 'center' });
      setTimeout(() => {
        const first = login.querySelector('input,button,select,textarea');
        if (first && typeof first.focus === 'function') first.focus({ preventScroll: true });
      }, 300);
    });

    return brief;
  }

  function showBrief() {
    if (window.gfieldPreLoginStarted) return;

    const intro = getIntro();
    const page2 = getPage2();
    const login = getLoginCard();
    const brief = ensureBrief();

    if (intro) {
      intro.style.display = 'none';
      intro.hidden = true;
    }
    if (page2) {
      page2.style.display = 'none';
      page2.hidden = true;
    }
    if (brief) {
      brief.style.display = 'block';
      brief.hidden = false;
    }
    if (login) {
      login.classList.add('prelogin-locked');
      login.style.display = 'none';
      login.hidden = true;
    }
    window.scrollTo(0, 0);
  }

  function shouldForceBrief() {
    if (window.gfieldPreLoginStarted) return false;

    const intro = getIntro();
    if (!intro) return true;

    const text = (intro.innerText || '').trim();
    if (text.includes('진단 시작까지') && text.includes('1')) return true;
    if (Date.now() - startedAt >= INTRO_TIMEOUT_MS) return true;
    return false;
  }

  function tick() {
    if (shouldForceBrief()) showBrief();
  }

  window.addEventListener('load', () => {
    ensureBrief();
    setTimeout(showBrief, INTRO_TIMEOUT_MS);
    setInterval(tick, POLL_MS);
  });
})();

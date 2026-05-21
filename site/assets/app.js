(function () {
  const parser = new DOMParser();
  let bottomReachedAt = 0;
  let navigationLock = false;

  function bindSearch() {
    const search = document.querySelector("[data-search]");
    if (!search) {
      return;
    }

    search.addEventListener("input", () => {
      const value = search.value.trim().toLowerCase();
      document.querySelectorAll(".lesson-link").forEach((link) => {
        const text = link.textContent.toLowerCase();
        link.classList.toggle("hidden", value.length > 0 && !text.includes(value));
      });
    });
  }

  function samePageShell(url) {
    return url.origin === window.location.origin && url.pathname.startsWith(basePath());
  }

  function basePath() {
    const parts = window.location.pathname.split("/").filter(Boolean);
    const repo = parts[0] || "";
    return repo ? `/${repo}/` : "/";
  }

  function isNavigableLink(anchor) {
    if (!anchor || anchor.target || anchor.hasAttribute("download")) {
      return false;
    }

    const url = new URL(anchor.href, window.location.href);
    if (!samePageShell(url)) {
      return false;
    }

    if (url.pathname === window.location.pathname && url.hash) {
      return false;
    }

    return true;
  }

  function updatePage(nextDocument, url, push) {
    const nextDoc = nextDocument.querySelector(".doc");
    const nextSidebar = nextDocument.querySelector("[data-sidebar]");
    const currentDoc = document.querySelector(".doc");
    const currentSidebar = document.querySelector("[data-sidebar]");

    if (!nextDoc || !nextSidebar || !currentDoc || !currentSidebar) {
      window.location.href = url.href;
      return;
    }

    document.title = nextDocument.title;
    document.documentElement.lang = nextDocument.documentElement.lang;
    currentDoc.innerHTML = nextDoc.innerHTML;
    currentSidebar.innerHTML = nextSidebar.innerHTML;

    if (push) {
      window.history.pushState({}, "", url.href);
    }

    bindSearch();
    bottomReachedAt = 0;
    window.scrollTo({ top: 0, behavior: "auto" });
  }

  async function navigateTo(url, push) {
    if (navigationLock) {
      return;
    }

    navigationLock = true;
    document.body.classList.add("is-loading");

    try {
      const response = await fetch(url.href, { headers: { "X-Requested-With": "fetch" } });
      if (!response.ok) {
        throw new Error(`Navigation failed: ${response.status}`);
      }

      const html = await response.text();
      const nextDocument = parser.parseFromString(html, "text/html");
      updatePage(nextDocument, url, push);
    } catch (_error) {
      window.location.href = url.href;
    } finally {
      document.body.classList.remove("is-loading");
      navigationLock = false;
    }
  }

  function currentLessonIndex() {
    const links = Array.from(document.querySelectorAll(".lesson-link"));
    const current = document.querySelector('.lesson-link[aria-current="page"]');
    return { links, index: links.indexOf(current) };
  }

  function navigateNextLesson() {
    const { links, index } = currentLessonIndex();
    if (index < 0 || index >= links.length - 1) {
      return;
    }

    const next = links[index + 1];
    const url = new URL(next.href, window.location.href);
    navigateTo(url, true);
  }

  function atPageBottom() {
    const doc = document.documentElement;
    return window.innerHeight + window.scrollY >= doc.scrollHeight - 2;
  }

  document.addEventListener("click", (event) => {
    const anchor = event.target.closest("a");
    if (!isNavigableLink(anchor)) {
      return;
    }

    event.preventDefault();
    navigateTo(new URL(anchor.href, window.location.href), true);
  });

  window.addEventListener("popstate", () => {
    navigateTo(new URL(window.location.href), false);
  });

  window.addEventListener("scroll", () => {
    if (atPageBottom()) {
      if (!bottomReachedAt) {
        bottomReachedAt = Date.now();
      }
      return;
    }

    bottomReachedAt = 0;
  }, { passive: true });

  window.addEventListener("wheel", (event) => {
    if (event.deltaY <= 0 || !atPageBottom()) {
      return;
    }

    if (bottomReachedAt && Date.now() - bottomReachedAt > 450) {
      event.preventDefault();
      navigateNextLesson();
    }
  }, { passive: false });

  bindSearch();
})();

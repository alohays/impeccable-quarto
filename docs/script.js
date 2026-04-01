/**
 * impeccable-quarto landing page — interactive behavior
 * Vanilla JavaScript, no dependencies.
 */

document.addEventListener("DOMContentLoaded", () => {
  // ----------------------------------------------------------------
  // Utility: debounce
  // ----------------------------------------------------------------
  function debounce(fn, delay) {
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => fn(...args), delay);
    };
  }

  // ================================================================
  // 1. Scroll-based Fade-in Animations
  // ================================================================
  const fadeElements = document.querySelectorAll(".fade-in");

  if (fadeElements.length) {
    const fadeObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target;
            const delay = parseInt(el.dataset.delay, 10) || 0;
            setTimeout(() => el.classList.add("visible"), delay);
            fadeObserver.unobserve(el);
          }
        });
      },
      { threshold: 0.1 }
    );

    fadeElements.forEach((el) => fadeObserver.observe(el));
  }

  // ================================================================
  // 2. Smooth Scroll for Navigation
  // ================================================================
  const navLinks = document.querySelectorAll('a[href^="#"]');
  const topNav = document.querySelector("nav.top-nav");

  function getNavHeight() {
    return topNav ? topNav.offsetHeight : 0;
  }

  navLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      const href = link.getAttribute("href");
      if (href === "#") return;
      const target = document.querySelector(href);
      if (!target) return;

      e.preventDefault();
      const top =
        target.getBoundingClientRect().top +
        window.scrollY -
        getNavHeight();

      window.scrollTo({ top, behavior: "smooth" });

      // Close mobile menu if open
      if (topNav) topNav.classList.remove("menu-open");
    });
  });

  // ================================================================
  // 3. FAQ Accordion
  // ================================================================
  const faqItems = document.querySelectorAll(".faq-item");

  faqItems.forEach((item) => {
    const question = item.querySelector(".faq-question");
    if (!question) return;

    question.addEventListener("click", () => {
      const isActive = item.classList.contains("active");

      // Close all other items
      faqItems.forEach((other) => {
        if (other !== item) other.classList.remove("active");
      });

      // Toggle current item
      item.classList.toggle("active", !isActive);
    });
  });

  // ================================================================
  // 4. Code Block Copy Button
  // ================================================================
  const codeBlocks = document.querySelectorAll(".code-block");

  codeBlocks.forEach((block) => {
    const codeEl = block.querySelector("code");
    if (!codeEl) return;

    const btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.textContent = "Copy";
    btn.setAttribute("aria-label", "Copy code to clipboard");
    block.style.position = "relative";
    block.appendChild(btn);

    btn.addEventListener("click", () => {
      const text = codeEl.textContent;
      navigator.clipboard.writeText(text).then(() => {
        btn.textContent = "Copied!";
        setTimeout(() => {
          btn.textContent = "Copy";
        }, 2000);
      });
    });
  });

  // ================================================================
  // 5. Navigation Scroll Effect
  // ================================================================
  if (topNav) {
    const handleNavScroll = debounce(() => {
      topNav.classList.toggle("scrolled", window.scrollY > 50);
    }, 10);

    window.addEventListener("scroll", handleNavScroll, { passive: true });
    // Apply immediately in case page loads mid-scroll
    topNav.classList.toggle("scrolled", window.scrollY > 50);
  }

  // ================================================================
  // 6. Active Section Highlighting
  // ================================================================
  const sections = document.querySelectorAll("section[id]");

  if (sections.length) {
    const sectionObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const id = entry.target.getAttribute("id");
          const link = document.querySelector(`a[href="#${id}"]`);
          if (!link) return;

          if (entry.isIntersecting) {
            // Remove active from all nav links, then set current
            navLinks.forEach((l) => l.classList.remove("active"));
            link.classList.add("active");
          }
        });
      },
      {
        rootMargin: `-${getNavHeight()}px 0px -40% 0px`,
        threshold: 0.1,
      }
    );

    sections.forEach((section) => sectionObserver.observe(section));
  }

  // ================================================================
  // 7. Theme Card Hover Preview
  // ================================================================
  const themeCards = document.querySelectorAll(".theme-card");

  themeCards.forEach((card) => {
    card.addEventListener("mouseenter", () => card.classList.add("hovered"));
    card.addEventListener("mouseleave", () => card.classList.remove("hovered"));
  });

  // ================================================================
  // 8. Counter Animation for Scoring
  // ================================================================
  const counters = document.querySelectorAll(".counter");

  if (counters.length) {
    const counterObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;

          const el = entry.target;
          if (el.dataset.animated) return;
          el.dataset.animated = "true";

          const target = parseInt(el.dataset.target, 10) || 0;
          const duration = 1500; // 1.5 seconds
          const startTime = performance.now();

          function easeOut(t) {
            return 1 - Math.pow(1 - t, 3);
          }

          function step(now) {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const value = Math.round(easeOut(progress) * target);
            el.textContent = value;

            if (progress < 1) {
              requestAnimationFrame(step);
            } else {
              el.textContent = target;
            }
          }

          requestAnimationFrame(step);
          counterObserver.unobserve(el);
        });
      },
      { threshold: 0.1 }
    );

    counters.forEach((el) => counterObserver.observe(el));
  }

  // ================================================================
  // 9. Mobile Menu Toggle
  // ================================================================
  const menuToggle = document.querySelector(".menu-toggle");

  if (menuToggle && topNav) {
    menuToggle.addEventListener("click", (e) => {
      e.stopPropagation();
      topNav.classList.toggle("menu-open");
    });

    // Close menu on nav link click
    navLinks.forEach((link) => {
      link.addEventListener("click", () => {
        topNav.classList.remove("menu-open");
      });
    });

    // Close menu when clicking outside
    document.addEventListener("click", (e) => {
      if (
        topNav.classList.contains("menu-open") &&
        !topNav.contains(e.target)
      ) {
        topNav.classList.remove("menu-open");
      }
    });
  }

  // ================================================================
  // 10. Typing Effect for Hero
  // ================================================================
  const typingEl = document.querySelector(".typing-text");

  if (typingEl) {
    const strings = [
      "Typography-First",
      "OKLCH-Colored",
      "Objectively Scored",
      "Semantically Structured",
    ];
    let stringIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    // Ensure cursor is present
    if (!typingEl.querySelector(".cursor")) {
      const cursor = document.createElement("span");
      cursor.className = "cursor";
      cursor.textContent = "|";
      typingEl.appendChild(cursor);
    }

    function getTextNode() {
      // Use the first text node, or create one before the cursor
      const cursor = typingEl.querySelector(".cursor");
      if (typingEl.firstChild && typingEl.firstChild.nodeType === Node.TEXT_NODE) {
        return typingEl.firstChild;
      }
      const textNode = document.createTextNode("");
      typingEl.insertBefore(textNode, cursor);
      return textNode;
    }

    const textNode = getTextNode();

    function typeStep() {
      const current = strings[stringIndex];

      if (!isDeleting) {
        // Typing forward
        charIndex++;
        textNode.textContent = current.slice(0, charIndex);

        if (charIndex >= current.length) {
          // Finished typing — pause, then start deleting
          isDeleting = true;
          setTimeout(typeStep, 2000);
          return;
        }
        setTimeout(typeStep, 50);
      } else {
        // Deleting backward
        charIndex--;
        textNode.textContent = current.slice(0, charIndex);

        if (charIndex <= 0) {
          // Finished deleting — move to next string
          isDeleting = false;
          stringIndex = (stringIndex + 1) % strings.length;
          setTimeout(typeStep, 300);
          return;
        }
        setTimeout(typeStep, 30);
      }
    }

    typeStep();
  }
});

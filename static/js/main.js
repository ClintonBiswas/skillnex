/* =========================================================
   NAVBAR
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    const navbar = document.getElementById("siteNavbar");
    const navbarMenu = document.getElementById("mainNavbar");
    const navbarToggler = document.querySelector(".site-navbar__toggler");

    if (!navbar || !navbarMenu || !navbarToggler) {
        return;
    }


    /* =====================================================
       1. NAVBAR SCROLL EFFECT
       ===================================================== */

    const handleNavbarScroll = () => {
        navbar.classList.toggle(
            "is-scrolled",
            window.scrollY > 30
        );
    };

    handleNavbarScroll();

    window.addEventListener("scroll", handleNavbarScroll, {
        passive: true
    });


    /* =====================================================
       2. CLOSE MENU
       ===================================================== */

    const closeMenu = () => {

        if (navbarMenu.classList.contains("show")) {

            const bootstrapCollapse =
                bootstrap.Collapse.getOrCreateInstance(navbarMenu);

            bootstrapCollapse.hide();
        }
    };


    /* =====================================================
       3. CLOSE WHEN CLICKING A NAVIGATION LINK
       ===================================================== */

    navbarMenu
        .querySelectorAll(".nav-link")
        .forEach((link) => {

            link.addEventListener("click", () => {
                closeMenu();
            });

        });


    /* =====================================================
       4. CLOSE WHEN CLICKING OUTSIDE NAVBAR
       ===================================================== */

    document.addEventListener("click", (event) => {

        const menuIsOpen =
            navbarMenu.classList.contains("show");

        const clickedInsideNavbar =
            navbar.contains(event.target);

        if (menuIsOpen && !clickedInsideNavbar) {
            closeMenu();
        }

    });


    /* =====================================================
       5. CLOSE WITH ESCAPE KEY
       ===================================================== */

    document.addEventListener("keydown", (event) => {

        if (event.key === "Escape") {
            closeMenu();
        }

    });

});
/* =========================================================
   COPYRIGHT YEAR
   ========================================================= */

const currentYear = document.getElementById("currentYear");

if (currentYear) {
    currentYear.textContent = new Date().getFullYear();
}

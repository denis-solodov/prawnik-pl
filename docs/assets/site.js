const { copied, copyCommand, copyFail } = document.body.dataset;

if (navigator.clipboard?.writeText) {
  for (const button of document.querySelectorAll("button[data-copy]")) {
    const row = button.closest(".copy-line");
    const source = document.getElementById(button.dataset.copy);
    const status = row.querySelector('[role="status"]');

    row.hidden = false;
    button.addEventListener("click", async () => {
      status.textContent = "";
      try {
        await navigator.clipboard.writeText(source.textContent.trim());
        status.textContent = source.id === "install-command" ? copyCommand : copied;
      } catch {
        status.textContent = copyFail;
      }
    });
  }
}

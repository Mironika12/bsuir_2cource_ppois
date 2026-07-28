let studentId = "";

function showError(inputId, message) {
  const input = document.getElementById(inputId);
  const error = document.getElementById(inputId + "Error");

  if (input) input.classList.add("error");
  if (error) error.textContent = message;
}

function clearError(inputId) {
  const input = document.getElementById(inputId);
  const error = document.getElementById(inputId + "Error");

  if (input) input.classList.remove("error");
  if (error) error.textContent = "";
}

async function login() {
    studentId = document.getElementById("studentId").value;
    const pin = document.getElementById("pin").value;

    const res = await fetch(`/login?student_id=${studentId}&pin=${pin}`, {
        method: "POST"
    });

    if (!res.ok) {
        alert("Ошибка входа");
        return;
    }

    document.getElementById("dashboard").style.display = "block";

    loadProject();
}

async function loadProject() {
    const res = await fetch(`/projects/${studentId}`);
    const data = await res.json();

    renderProject(data);
}

function renderProject(data) {
    document.getElementById("projectInfo").innerHTML = `
        <p><b>Тема:</b> ${data.theme || "-"}</p>
        <p><b>Статус:</b> ${data.state}</p>
        <p><b>Дедлайн:</b> ${data.deadline?.deadline_date || "-"}</p>

        <h4>План:</h4>
        <ul>
          ${data.plan.map(i => `
            <li>${i.num}. ${i.task}</li>
          `).join("")}
        </ul>

        <h4>Источники:</h4>
        <ul>
          ${data.references.map(r => `
            <li>${r.reference}</li>
          `).join("")}
        </ul>

        <h4>Текст:</h4>
        <ul>
          ${data.text_sections.map(t => `<li>${t}</li>`).join("")}
        </ul>
    `;
}

async function setTheme() {
  const theme = document.getElementById("themeInput").value.trim();

  clearError("themeInput");

  if (!theme) {
    showError("themeInput", "Введите тему проекта");
    return;
  }

  const response = await fetch(
    `/projects/${studentId}/theme?theme=${encodeURIComponent(theme)}`,
    {
      method: "PATCH"
    }
  );

  if (!response.ok) {
    const errorText = await response.text();
    console.log(errorText.detail);
    showError("themeInput", errorText);
    return;
  }
  
  loadProject();
}

async function addPlanItem() {
    const num = document.getElementById("taskNum").value;
    const task = document.getElementById("taskText").value;
    const deadline = document.getElementById("taskDeadline").value;

    clearError("taskNum");
    clearError("taskText");
    clearError("taskDeadline");

    // let valid = true;

    if (!num || num == 0) {
        showError("taskNum", "Укажите номер пункта");
        // valid = false;
        return;
    }

    if (!task) {
        showError("taskText", "Введите описание задачи");
        // valid = false;
        return;
    }

    if (!deadline) {
        showError("taskDeadline", "Выберите дату");
        // valid = false;
        return;
    }

    // if (!valid) {
    //     return;
    // }

    const item = {
        num: Number(num),
        task: task,
        deadline: deadline,
        notes: document.getElementById("taskNotes").value
    };

    const response = await fetch(`/projects/${studentId}/plan`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(item)
    });

    if (!response.ok) {
        const errorText = await response.json();

        console.log(errorText.detail);
        showError("taskText", errorText.detail);

        return;
    }

    loadProject();
}

async function addReference() {
    clearError("refInput");
    const reference = document.getElementById("refInput").value.trim();

    if (!reference) {
        showError(
            "refInput",
            "Введите источник"
        );
        return;
    }

    const ref = {
        reference: reference,
        is_read: false
    };

    const response = await fetch(`/projects/${studentId}/references`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(ref)
    });

    if (!response.ok) {
        const data = await response.json();
        showError(
            "refInput",
            data.detail
        );
        return;
    }

    loadProject();
}

async function writeSection() {

    clearError("sectionText");

    const text = document
        .getElementById("sectionText")
        .value
        .trim();

    if (!text) {
        showError(
            "sectionText",
            "Введите текст раздела"
        );

        return;
    }

    const response = await fetch(
        `/projects/${studentId}/write?text=${encodeURIComponent(text)}`,
        {
            method: "PATCH"
        }
    );

    if (!response.ok) {
        const data = await response.json();

        showError(
            "sectionText",
            data.detail
        );

        return;
    }

    document.getElementById("sectionText").value = "";

    loadProject();
}

async function setDeadline() {

    clearError("deadlineDate");

    const date = document.getElementById("deadlineDate").value;
   
    if (!date) {
        showError(
            "deadlineDate",
            "Выберите дату дедлайна"
        );

        return;
    }

    const response = await fetch(
        `/projects/${studentId}/deadline?deadline_date=${date}`,
        {
            method: "PATCH"
        }
    );

    if (!response.ok) {
        const data = await response.json();

        showError(
            "deadlineDate",
            data.detail
        );

        return;
    }

    loadProject();
}

async function addConsultation() {

    clearError("consultationDate");

    const date = document.getElementById("consultationDate").value;

    if (!date) {
        showError(
            "consultationDate",
            "Выберите дату консультации"
        );

        return;
    }

    const response = await fetch(
        `/projects/${studentId}/consultation?consultation_date=${date}`,
        {
            method: "PATCH"
        }
    );

    if (!response.ok) {
        const data = await response.json();

        showError(
            "consultationDate",
            data.detail
        );

        return;
    }

    loadProject();
}

async function submitProject() {

    const response = await fetch(
        `/projects/${studentId}/submit`,
        {
            method: "PATCH"
        }
    );

    if (!response.ok) {
        const data = await response.json();

        alert(data.detail);

        return;
    }

    loadProject();
}
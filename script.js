let tasks = [];


// Load tasks from the database
async function loadTasks() {

    const response = await fetch("/api/tasks");

    if (response.ok) {

        tasks = await response.json();

        displayTasks(tasks);

    } else {

        alert("Could not load tasks.");

    }
}


// Add a new task
async function addTask() {

    const taskInput = document.getElementById("taskInput");

    const taskText = taskInput.value.trim();

    if (taskText === "") {

        alert("Please enter a task.");

        return;
    }


    const response = await fetch("/api/tasks", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            title: taskText
        })

    });


    if (response.ok) {

        taskInput.value = "";

        await loadTasks();

    } else {

        alert("Could not add the task.");

    }
}


// Display tasks
function displayTasks(taskArray) {

    const taskList = document.getElementById("taskList");

    taskList.innerHTML = "";


    if (taskArray.length === 0) {

        taskList.innerHTML = `
            <li class="empty-message">
                No tasks found.
            </li>
        `;

        return;
    }


    taskArray.forEach(task => {

        const li = document.createElement("li");


        if (task.completed) {

            li.classList.add("completed");

        }


        li.innerHTML = `

            <span>${task.title}</span>

            <div class="task-buttons">

                <button onclick="toggleTask(${task.id})">
                    ${task.completed ? "Undo" : "Complete"}
                </button>

                <button onclick="editTask(${task.id})">
                    Edit
                </button>

                <button onclick="deleteTask(${task.id})">
                    Delete
                </button>

            </div>

        `;


        taskList.appendChild(li);

    });
}


// Complete / Undo task
async function toggleTask(id) {

    const task = tasks.find(task => task.id === id);


    if (!task) {

        return;

    }


    const response = await fetch(`/api/tasks/${id}`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            completed: !task.completed

        })

    });


    if (response.ok) {

        await loadTasks();

    } else {

        alert("Could not update the task.");

    }
}


// Edit task
async function editTask(id) {

    const task = tasks.find(task => task.id === id);


    if (!task) {

        return;

    }


    const newTitle = prompt(
        "Edit your task:",
        task.title
    );


    if (newTitle === null) {

        return;

    }


    const updatedTitle = newTitle.trim();


    if (updatedTitle === "") {

        alert("Task title cannot be empty.");

        return;

    }


    const response = await fetch(`/api/tasks/${id}`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            title: updatedTitle

        })

    });


    if (response.ok) {

        await loadTasks();

    } else {

        alert("Could not edit the task.");

    }
}


// Delete task
async function deleteTask(id) {

    const confirmed = confirm(
        "Are you sure you want to delete this task?"
    );


    if (!confirmed) {

        return;

    }


    const response = await fetch(`/api/tasks/${id}`, {

        method: "DELETE"

    });


    if (response.ok) {

        await loadTasks();

    } else {

        alert("Could not delete the task.");

    }
}


// Filter tasks
function showTasks(filter) {

    let filteredTasks = tasks;


    if (filter === "pending") {

        filteredTasks = tasks.filter(
            task => !task.completed
        );

    }


    if (filter === "completed") {

        filteredTasks = tasks.filter(
            task => task.completed
        );

    }


    displayTasks(filteredTasks);
}


// Load tasks when page opens
loadTasks();
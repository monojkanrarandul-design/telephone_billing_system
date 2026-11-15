// Toggle password visibility (The Almighty's Sight)
function togglePassword(inputId, iconElement) {
    const input = document.getElementById(inputId);
    if (input.type === "password") {
        input.type = "text";
        iconElement.textContent = "🔒"; // Changes icon when visible
    } else {
        input.type = "password";
        iconElement.textContent = "👁️"; // Changes icon when hidden
    }
}
document.addEventListener("DOMContentLoaded", () => {
    
    // 1. Kurohitsugi (Triggered by Login/Register form submission)
    const authForm = document.getElementById("auth-form");
    if (authForm) {
        const kOverlay = document.createElement("div");
        kOverlay.className = "kurohitsugi-overlay";
        const kBox = document.createElement("div");
        kBox.className = "kurohitsugi-box";
        kOverlay.appendChild(kBox);
        document.body.appendChild(kOverlay);

        // Preload audio
        const kuroSound = new Audio('/static/kurohitsugi.mp3'); 

        authForm.addEventListener("submit", (e) => {
            e.preventDefault();
            kuroSound.play(); // Play the bass drop
            kOverlay.classList.add("kurohitsugi-active");
            
            // Wait for coffin to seal (1.8s) then submit
            setTimeout(() => { authForm.submit(); }, 1800);
        });
    }

    // 2. Garganta (Triggered by clicking Dashboard)
    const gargantaBtn = document.getElementById("btn-garganta");
    if (gargantaBtn) {
        const gOverlay = document.createElement("div");
        gOverlay.className = "garganta-overlay";
        document.body.appendChild(gOverlay);

        gargantaBtn.addEventListener("click", (e) => {
            e.preventDefault();
            const target = gargantaBtn.href;
            gOverlay.classList.add("garganta-active");
            
            setTimeout(() => { window.location.href = target; }, 1200);
        });
    }

    // 3. Kyoka Suigetsu Shatter (Triggered by clicking Add Data)
    const shatterBtn = document.getElementById("btn-shatter");
    if (shatterBtn) {
        // Create the crack overlay
        const crackOverlay = document.createElement("div");
        crackOverlay.className = "glass-crack";
        document.body.appendChild(crackOverlay);

        // Preload audio
        const shatterSound = new Audio('/static/shatter.mp3');

        shatterBtn.addEventListener("click", (e) => {
            e.preventDefault();
            const target = shatterBtn.href;
            
            shatterSound.play(); // Play the glass breaking sound
            crackOverlay.classList.add("crack-active"); // Show the crack lines
            document.querySelector(".container").classList.add("shatter-active"); // Break the container
            
            setTimeout(() => { window.location.href = target; }, 1100);
        });
    }

    // 4. Blackhole / Spaghettification (Triggered by Wipe History)
    const blackholeBtn = document.getElementById("btn-blackhole");
    if (blackholeBtn) {
        const bhOverlay = document.createElement("div");
        bhOverlay.className = "blackhole-center";
        document.body.appendChild(bhOverlay);

        blackholeBtn.addEventListener("click", (e) => {
            e.preventDefault(); // Pause the route redirect
            const target = blackholeBtn.href;
            
            // Play the Aizen confirmation first
            if(confirm('Shatter, Kyoka Suigetsu. Are you sure you want to wipe all history?')) {
                // Spaghettify the UI container
                document.querySelector(".container").classList.add("spaghetti-suck");
                // Expand the blackhole
                bhOverlay.classList.add("blackhole-active");
                
                // Wait for the void to consume everything, then execute wipe
                setTimeout(() => { window.location.href = target; }, 2400);
            }
        });
    }// 5. Live Communications Intercept (Simulated Live Traffic)
    const simulateBtn = document.getElementById("btn-simulate");
    if (simulateBtn) {
        let simulationInterval;
        let isSimulating = false;

        simulateBtn.addEventListener("click", (e) => {
            e.preventDefault();
            isSimulating = !isSimulating;
            
            if (isSimulating) {
                // Turn button RED to indicate active recording
                simulateBtn.innerHTML = "🛑 Halt Interception";
                simulateBtn.style.color = "#ff3333";
                simulateBtn.style.borderColor = "#ff3333";
                simulateBtn.style.boxShadow = "0 0 15px rgba(255,51,51,0.4) inset";
                
                // Ping the server every 2.5 seconds
                simulationInterval = setInterval(async () => {
                    const response = await fetch('/simulate_live_traffic');
                    const data = await response.json();
                    
                    // Grab the table and insert a new row right beneath the headers
                    const table = document.querySelector("table");
                    const newRow = table.insertRow(1); 
                    newRow.className = "new-data-flash"; // Play the cyan flash animation
                    
                    // Populate the row with the newly generated Bleach data
                    newRow.innerHTML = `
                        <td>${data.bill_id}</td>
                        <td>${data.name}</td>
                        <td>${data.phone}</td>
                        <td>${data.call_duration}</td>
                        <td>₹${data.amount.toFixed(1)}</td>
                        <td><a href="/delete/${data.bill_id}" class="btn-delete">Delete</a></td>
                    `;
                }, 2500); // 2500 milliseconds = 2.5 seconds
            } else {
                // Reset button back to GREEN
                simulateBtn.innerHTML = "📡 Intercept Live Comms";
                simulateBtn.style.color = "#00ff00";
                simulateBtn.style.borderColor = "#00ff00";
                simulateBtn.style.boxShadow = "0 0 10px rgba(0,255,0,0.2) inset";
                clearInterval(simulationInterval);
            }
        });
    }

});
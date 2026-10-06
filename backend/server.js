const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");
const path = require("path");

const app = express();

app.use(cors());
app.use(express.json());

app.get("/options", (req, res) => {
    const pythonPath = path.join(__dirname, "../.venv/Scripts/python.exe");
    const pythonScript = path.join(__dirname, "../src/options_api.py");

    const python = spawn(pythonPath, [pythonScript], {
        cwd: path.join(__dirname, "..")
    });

    let output = "";
    let error = "";

    python.stdout.on("data", (data) => {
        output += data.toString();
    });

    python.stderr.on("data", (data) => {
        error += data.toString();
    });

    python.on("close", (code) => {
        if (code !== 0) {
            console.error("Options error:", error);

            return res.status(500).json({
                success: false,
                error: "Could not load options"
            });
        }

        try {
            const result = JSON.parse(output);
            res.json(result);
        } catch (err) {
            console.error("Invalid options response:", output);

            res.status(500).json({
                success: false,
                error: "Invalid options response"
            });
        }
    });
});

app.post("/predict", (req, res) => {
    console.log("Prediction request:", req.body);

    const pythonPath = path.join(__dirname, "../.venv/Scripts/python.exe");
    const pythonScript = path.join(__dirname, "../src/predict_api.py");

    const python = spawn(pythonPath, [pythonScript], {
        cwd: path.join(__dirname, "..")
    });

    let output = "";
    let error = "";

    python.stdout.on("data", (data) => {
        output += data.toString();
    });

    python.stderr.on("data", (data) => {
        error += data.toString();
    });

    python.on("close", (code) => {
        if (code !== 0) {
            console.error("Python error:", error);

            return res.status(500).json({
                success: false,
                error: "Prediction failed"
            });
        }

        try {
            const result = JSON.parse(output);
            res.json(result);
        } catch (err) {
            console.error("Invalid Python response:", output);

            res.status(500).json({
                success: false,
                error: "Invalid prediction response"
            });
        }
    });

    python.stdin.write(JSON.stringify(req.body));
    python.stdin.end();
});

app.get("/", (req, res) => {
    res.json({
        message: "NEET College Predictor API is running"
    });
});

app.listen(5000, () => {
    console.log("Server running at http://localhost:5000");
});
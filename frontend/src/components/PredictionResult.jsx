import React from 'react';
import './PredictionResult.css';

const PredictionResult = ({ predictedClass, probabilities, onReset }) => {
    return (
        <div className="prediction-result">
            <h2>Analysis Result</h2>

            <div className="predicted-class">
                <h3>Prediction</h3>
                <span className={`prediction-badge ${predictedClass === 'Lep' ? 'leprosy' : 'non-leprosy'}`}>
                    {predictedClass === 'Lep' ? 'Leprosy Detected' : 'Non-Leprosy'}
                </span>
            </div>

            <div className="probabilities">
                <h4>Confidence Levels:</h4>
                {Object.entries(probabilities).map(([label, prob]) => {
                    const isLeprosy = label === 'Lep' || label.includes('Lep');
                    return (
                        <div key={label} className="probability-item">
                            <div className="probability-label">
                                <span>{label}</span>
                                <span>{(prob * 100).toFixed(2)}%</span>
                            </div>
                            <div className="probability-bar">
                                <div
                                    className={`probability-fill ${isLeprosy ? 'leprosy-bar' : 'non-leprosy-bar'}`}
                                    style={{ width: `${prob * 100}%` }}
                                ></div>
                            </div>
                        </div>
                    );
                })}
            </div>

            <div className="disclaimer">
                <p>
                    <strong>Disclaimer:</strong> This is an AI-based decision support tool and not a substitute for professional medical diagnosis.
                    Please consult a qualified healthcare professional for proper diagnosis and treatment.
                </p>
            </div>

            <button onClick={onReset} className="reset-btn">
                Analyze Another Image
            </button>
        </div>
    );
};

export default PredictionResult;

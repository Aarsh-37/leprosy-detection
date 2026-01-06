import React, { useState } from 'react';
import { predictImage } from '../api/client';
import PredictionResult from './PredictionResult';
import './ImageUpload.css';

const ImageUpload = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setSelectedFile(file);
            setPreview(URL.createObjectURL(file));
            setResult(null);
            setError(null);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            setSelectedFile(file);
            setPreview(URL.createObjectURL(file));
            setResult(null);
            setError(null);
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
    };

    const handleSubmit = async () => {
        if (!selectedFile) {
            setError('Please select an image first');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const data = await predictImage(selectedFile);
            setResult(data);
        } catch (err) {
            setError(err.response?.data?.error || 'An error occurred while analyzing the image');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="image-upload-container">
            <h1>Leprosy Skin Lesion Detection</h1>

            <div
                className="drop-zone"
                onDrop={handleDrop}
                onDragOver={handleDragOver}
            >
                {preview ? (
                    <img src={preview} alt="Preview" className="preview-image" />
                ) : (
                    <div className="drop-zone-placeholder">
                        <p>Drag and drop an image here or click to select</p>
                        <input
                            type="file"
                            accept="image/*"
                            onChange={handleFileChange}
                            className="file-input"
                        />
                    </div>
                )}
            </div>

            {preview && !result && (
                <div className="file-info">
                    <p>Selected: {selectedFile?.name}</p>
                    <input
                        type="file"
                        accept="image/*"
                        onChange={handleFileChange}
                        className="file-input-button"
                        id="file-input"
                    />
                    <label htmlFor="file-input" className="change-image-btn">
                        Change Image
                    </label>
                </div>
            )}

            {preview && !result && (
                <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className="analyze-btn"
                >
                    {loading ? 'Analyzing...' : 'Analyze Lesion'}
                </button>
            )}

            {loading && (
                <div className="loading-spinner">
                    <div className="spinner"></div>
                    <p>Analyzing image...</p>
                </div>
            )}

            {error && (
                <div className="error-message">
                    <p>{error}</p>
                </div>
            )}

            {result && (
                <PredictionResult
                    predictedClass={result.predicted_class}
                    probabilities={result.probabilities}
                    onReset={() => {
                        setSelectedFile(null);
                        setPreview(null);
                        setResult(null);
                        setError(null);
                    }}
                />
            )}
        </div>
    );
};

export default ImageUpload;

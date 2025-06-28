from fpdf import FPDF
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import cv2

def generate_enhanced_summary(analysis, comments, base_path):
    # Generate visualizations
    create_timeline(analysis, f"{base_path}_timeline.png")
    create_object_cloud(analysis, f"{base_path}_objects.png")
    
    # Create PDF with visualizations
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Journey Intelligence Report", 0, 1, 'C')
    pdf.ln(10)
    
    # Key metrics table
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Journey Metrics", 0, 1)
    pdf.set_font("Arial", '', 10)
    pdf.cell(95, 10, f"Duration: {analysis['duration']:.2f} seconds", 1)
    pdf.cell(95, 10, f"Distance: {analysis['distance']:.2f} km", 1, 1)
    pdf.cell(95, 10, f"Avg Speed: {analysis['avg_speed']:.2f} km/h", 1)
    pdf.cell(95, 10, f"Key Events: {len(analysis['key_events'])}", 1, 1)
    pdf.ln(10)
    
    # Visualizations
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Object Detection Summary", 0, 1)
    pdf.image(f"{base_path}_objects.png", x=10, w=190)
    pdf.ln(5)
    
    pdf.cell(0, 10, "Event Timeline", 0, 1)
    pdf.image(f"{base_path}_timeline.png", x=10, w=190)
    pdf.ln(5)
    
    # Comments section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "User Comments & Insights", 0, 1)
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(0, 8, comments)
    
    # Save PDF
    pdf.output(f"{base_path}.pdf")
    
def create_timeline(analysis, output_path):
    fig, ax = plt.subplots(figsize=(10, 4))
    times = [e['timestamp'] for e in analysis['key_events']]
    events = [e['event'] for e in analysis['key_events']]
    
    ax.plot(times, np.zeros(len(times)), '|', markersize=50)
    for i, (time, event) in enumerate(zip(times, events)):
        ax.text(time, 0.1, event, rotation=45, ha='right')
    
    ax.set_yticks([])
    ax.set_xlabel('Time (seconds)')
    ax.set_title('Key Event Timeline')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
def create_object_cloud(analysis, output_path):
    object_counts = analysis['object_summary']
    wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(object_counts)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.title('Detected Objects Frequency')
    plt.savefig(output_path)
    plt.close()
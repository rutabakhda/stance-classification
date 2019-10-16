package de.aitools.aq.wat.components;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import de.aitools.aq.wat.data.Component;
import de.aitools.aq.wat.data.ComponentState;
import de.aitools.aq.wat.io.RecordsFile;


public class SegmentLabeling extends Component {
  
  private static final String JS_VALUE_FUNCTION_NAME = "setSegmentLabelingValue";

  private static final String VALUE_UNANNOTATED = "unannotated";

  private static final String LABEL_CONTINUED = "continued";

  private static final String CONFIG_LABEL_NAMES = "labels";

  private static final String CONFIG_LABEL_PREFIX = "label.";

  private static final String CONFIG_LABEL_DISPLAY_NAME_SUFFIX = ".name";

  private static final String CONFIG_LABEL_TITLE_SUFFIX = ".title";

  private static final String CONFIG_LABEL_DISABLED_TITLE_SUFFIX = ".disabled.title";
  
  private List<List<Segment>> segmentParagraphs;
  
  private List<Label> labelsInParagraph;
  
  private List<Label> labelsEndOfParagraph;

  public SegmentLabeling(
      final String name,
      final File projectDirectory, final File taskDirectory, 
      final Map<String, RecordsFile> recordFilesByAnnotator)
  throws IOException {
    super(name, projectDirectory, taskDirectory, recordFilesByAnnotator,
        JS_VALUE_FUNCTION_NAME);
    this.addCssIncludes("/css/segment-labeling.css");
    this.addJsIncludes("/js/segment-labeling.js");
    this.addJsInitFunctions("segmentLabelingInitialize");
  }

  @Override
  public void printHtmlInPanel(final PrintWriter output) {
    boolean isfirstSegment = true;
    for (final List<Segment> segmentParagraph : this.segmentParagraphs) {
      output.append("<div class=\"segments-paragraph\">");
      for (final Segment segment : segmentParagraph) {
        if (isfirstSegment == true){
          segment.printHtml_first_segment(output, this.getName());
        }else{
          segment.printHtml(output, this.getName());
        }
        isfirstSegment = false;
      }
      output.append("</div>\n");
    }
  }
  
  @Override
  protected void loadForTask(final Properties config,
      final File projectDirectory, final File taskDirectory)
  throws IOException {
    this.segmentParagraphs = new ArrayList<>();
    this.labelsInParagraph = new ArrayList<>();
    this.labelsEndOfParagraph = new ArrayList<>();
    this.loadLabels(config);
    this.readSegments(taskDirectory);
  }
  
  private void loadLabels(final Properties config) {
    final String[] labelNames =
        config.getProperty(CONFIG_LABEL_NAMES, "").split("\\s+");
    if (labelNames.length < 2) {
      throw new IllegalArgumentException(
          "Less than two labels defined with property '"
              + CONFIG_LABEL_NAMES + "'");
    }
    
    for (final String labelName : labelNames) {
      final String displayName = config.getProperty(
          CONFIG_LABEL_PREFIX + labelName + CONFIG_LABEL_DISPLAY_NAME_SUFFIX,
          labelName);
      final String title = config.getProperty(
          CONFIG_LABEL_PREFIX + labelName + CONFIG_LABEL_TITLE_SUFFIX,
          "");
      final Label label = new Label(labelName, displayName, title, false);
      this.labelsInParagraph.add(label);
      if (!labelName.equals(LABEL_CONTINUED)) {
        this.labelsEndOfParagraph.add(label);
      } else {
        final String titleDisabled = config.getProperty(
            CONFIG_LABEL_PREFIX + labelName + CONFIG_LABEL_DISABLED_TITLE_SUFFIX,
            "Segments at the end of a paragraph can not be continued.");
        this.labelsEndOfParagraph.add(
            new Label(labelName, displayName, titleDisabled, true));
      }
    }
  }
  
  private void readSegments(final File taskDirectory)
  throws IOException {
    try (final BufferedReader reader = new BufferedReader(new FileReader(
        new File(taskDirectory, this.getName() + ".txt")))) {
      List<Segment> paragraph = new ArrayList<>();

      String line;

      final Segment a = new Segment(String.valueOf(0), "<font color=red><b>Label of Paragraph</b></font>");
      paragraph.add(a);

      int s = 1;
      while ((line = reader.readLine()) != null) {
        line = line.trim();
        if (line.isEmpty()) {
          if (!paragraph.isEmpty()) {
            paragraph.get(paragraph.size() - 1).setLabels(
                this.labelsEndOfParagraph);
            this.segmentParagraphs.add(paragraph);
          }
          paragraph = new ArrayList<>();
        } else {
          if (!paragraph.isEmpty()) {
            paragraph.get(paragraph.size() - 1).setLabels(
                this.labelsInParagraph);
          }
          final Segment segment = new Segment(String.valueOf(s), line);
          paragraph.add(segment);
          this.addUnit(segment);
          ++s;
        }
      }
      
      if (!paragraph.isEmpty()) {
        paragraph.get(paragraph.size() - 1).setLabels(
            this.labelsEndOfParagraph);
        this.segmentParagraphs.add(paragraph);
      }
    }
  }

  @Override
  protected ComponentState createNewStateInstance() {
    return new SegmentLabelingState(this);
  }
  
  private static class SegmentLabelingState extends ComponentState {
    
    private final int numSegments;
    
    private int numUnannotated;
    
    public SegmentLabelingState(final SegmentLabeling component) {
      this.numSegments = component.getSize() + 1;
      this.numUnannotated = this.numSegments;
    }
    
    @Override
    public String getProgress() {
      return (this.numSegments - this.numUnannotated) + "/"
          + this.numSegments  + " segments";
    }

    @Override
    public boolean isComplete() {
      return this.numUnannotated == 0;
    }

    @Override
    protected void updateProgress(final String key, final String value) {
      final String oldValue = this.getValue(key);
      final boolean wasAnnotated = this.isAnnotated(oldValue);
      final boolean isAnnotated = this.isAnnotated(value);
      if (isAnnotated && !wasAnnotated) {
        --this.numUnannotated;
      } else if (!isAnnotated && wasAnnotated) {
        ++this.numUnannotated;
      }
    }

    private boolean isAnnotated(final String value) {
      return value != null && !value.equals(SegmentLabeling.VALUE_UNANNOTATED);
    }
    
  }
  
  private static class Segment extends Unit {
    
    private String text;
    
    private List<Label> labels;
    
    private Segment(final String key, final String text) {
      super(key);
      this.setText(text.replaceAll("\\s+", " ").trim());
      this.labels = new ArrayList<>();
    }
    
    public void setText(final String text) {
      if (text == null) { throw new NullPointerException(); }
      this.text = text;
    }
    
    private void setLabels(final List<Label> labels) {
      this.labels = labels;
    }
    
    public void printHtml(final PrintWriter output, final String componentName) {
      output.append("<span class=\"segment ").append(VALUE_UNANNOTATED)
        .append("\" id=\"").append(componentName).append(this.getKey())
        .append("\" title=\"").append("segment " + this.getKey()).append("\"")
        .append(" data-label=\"").append(VALUE_UNANNOTATED).append("\">");
      
      final int lastSpace = this.text.lastIndexOf(' ');
      if (lastSpace > 0) {
        output.append(this.text.substring(0, lastSpace)).append(' ');
      }
      output.append("<span class=\"nobreak\">");
      output.append(this.text.substring(lastSpace + 1));
      
      output.append("&nbsp;<span class=\"dropdown\">")
        .append("<img class=\"dropdown-toggle\" data-toggle=\"dropdown\"/>");
      output.append("<ul class=\"dropdown-menu\" role=\"menu\">");
      
      for (int l = 2; l < this.labels.size(); ++l) {
        final Label label = this.labels.get(l);
        final List<String> annotators = this.getAnnotators(label.name);
        label.printHtml(output, componentName, this.getKey(), annotators);
      }

      output.append("</ul>");
      output.append("</span>");

      output.append("</span>");
      output.append("</span>");
    }

    public void printHtml_first_segment(final PrintWriter output, final String componentName) {
      output.append("<div><span class=\"segment ").append(VALUE_UNANNOTATED)
        .append("\" id=\"").append(componentName).append(this.getKey())
        .append("\" title=\"").append("segment " + this.getKey()).append("\"")
        .append(" data-label=\"").append(VALUE_UNANNOTATED).append("\">");
      
      final int lastSpace = this.text.lastIndexOf(' ');
      if (lastSpace > 0) {
        output.append(this.text.substring(0, lastSpace)).append(' ');
      }
      output.append("<span class=\"nobreak\">");
      output.append(this.text.substring(lastSpace + 1));
      
      output.append("&nbsp;<span class=\"dropdown\">")
        .append("<img class=\"dropdown-toggle\" data-toggle=\"dropdown\"/>");
      output.append("<ul class=\"dropdown-menu\" role=\"menu\">");
      
      for (int l = 0; l < 2; ++l) {
        final Label label = this.labels.get(l);
        final List<String> annotators = this.getAnnotators(label.name);
        label.printHtml(output, componentName, this.getKey(), annotators);
      }

      output.append("</ul>");
      output.append("</span>");
      output.append("</div>");

      output.append("</span>");
      output.append("</span>");
    }
    
  }
  
  public static class Label {
    
    protected final String name;
    
    protected final String displayName;
    
    protected final String title;
    
    protected final boolean isDisabled;

    public Label(final String name, final String displayName,
        final String title, final boolean isDisabled) {
      if (name == null) { throw new NullPointerException(); }
      if (displayName == null) { throw new NullPointerException(); }
      if (title == null) { throw new NullPointerException(); }
      
      this.name = name;
      this.displayName = displayName;
      this.title = title;
      this.isDisabled = isDisabled;
    }
    
    public void printHtml(
        final PrintWriter output, final String componentName,
        final String segmentKey, final List<String> annotators) {
      final String id =
          "annotate-" + componentName + segmentKey + "-as-" + this.name;

      output.append("<li id=\"").append(id)
        .append("\" role=\"presentation\" class=\"").append(this.name);
      if (this.isDisabled) {
        output.append(" disabled");
      }
      output.append("\" title=\"").append(this.title);
      if (annotators != null) {
        output.append(" | annotated by: ")
          .append(String.join(", ", annotators));
      }
      output.append("\">");
  
      output.append("<a class=\"annotation-button\" role=\"menuitem\" ")
        .append("tabindex=\"-1\" ")
        .append("href=\"javascript:if(!$('#").append(id)
        .append("').hasClass('disabled')){update('").append(componentName)
        .append("', ").append(segmentKey)
        .append(", '").append(this.name).append("')}\">");
      output.append(this.displayName);
      if (annotators != null) {
        output.append(" (" + annotators.size() + ")");
      }
      output.append("</a>");
  
      output.append("</li>");
    }
    
  }

}

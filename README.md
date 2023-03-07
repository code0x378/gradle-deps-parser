# Gradle Dependencies Parser

This parses the dependencies of a build.gradle file and outputs them in different formats.

## Usage

```bash
python gdp.py -i normal -o kotlin -f output.txt <path to build.gradle file>
```
## Notes

* This does not modify the build.gradle file and only outputs to a file for review.
* This does not convert the entire script (i.e. from groovy to kotlin), only the dependencies section.
* This is not recursive.

## Example

**Groovy Short Input**

```groovy
implementation 'com.fasterxml.uuid:java-uuid-generator:4.0.1'
kapt 'com.github.rjeschke:txtmark:0.13'
compile 'org.apache.httpcomponents:httpclient:4.5.13'
```
**Kotlin Output**
```kotlin
implementation('com.fasterxml.uuid:java-uuid-generator:4.0.1')
kapt('com.github.rjeschke:txtmark:0.13')
compile('org.apache.httpcomponents:httpclient:4.5.13')
```
import sys
import pathlib
from xml.etree import ElementTree as et


if __name__ == "__main__":

    coverage_path = (
        pathlib.Path(__file__).parent.parent / "tests" / "_reports" / "coverage.xml"
    )

    cov_xml: et.Element = et.parse(coverage_path).getroot()
    package_info: et.Element = cov_xml.find(".//package[@name='.']")

    coverage = float(package_info.attrib["line-rate"])

    if coverage < 0.85:
        cov_percent = coverage * 100
        error_message = (
            f"test coverage must exceed 85% to publish, "
            f"current coverage is {cov_percent}%\n"
        )
        print(error_message)
        sys.stderr.write(error_message)

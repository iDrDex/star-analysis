import gzip, glob, os


def parseLine(line):
    return " ".join(line.replace('"', '').split()[1:])


def getRec(filename):
    inMatrix = False
    f = gzip.open(filename)
    rec = dict(
        series_title="",
        series_geo_accession="",
        series_status="",
        series_submission_date="",
        series_last_update_date="",
        series_pubmed_id="",
        series_type="",
        series_platform_id="",
        series_sample_taxid="",
        numProbes=0,
        numSamples=0

    )
    last = ""
    try:
        for line in f:
            # if line.startswith('''"ID_REF"'''):
            if not inMatrix and last.startswith("!series_matrix_table_begin"):
                inMatrix = True
                rec['numSamples'] = len(line.split()) - 1
                continue
            elif line.startswith("!series_matrix_table_end"):
                break
            elif inMatrix:
                rec['numProbes'] += 1
            elif line.startswith("!Series_title"):
                rec['series_title'] = parseLine(line)

            elif line.startswith("!Series_geo_accession"):
                rec['series_geo_accession'] = parseLine(line)

            elif line.startswith("!Series_status"):
                rec['series_status'] = parseLine(line)

            elif line.startswith("!Series_submission_date"):
                rec['series_submission_date'] = parseLine(line)

            elif line.startswith("!Series_last_update_date"):
                rec['series_last_update_date'] = parseLine(line)

            elif line.startswith("!Series_pubmed_id"):
                rec['series_pubmed_id'] = parseLine(line)

            elif line.startswith("!Series_type"):
                rec['series_type'] = parseLine(line)

            elif line.startswith("!Series_platform_id"):
                rec['series_platform_id'] = parseLine(line)

            elif line.startswith("!Series_sample_taxid"):
                rec['series_sample_taxid'] = parseLine(line)
            last = line
        rec['filename'] = os.path.basename(filename)
    except IOError:
        print "IOError:", filename
    return rec


def print_GEO_summary():
    headers = """
    filename
    numProbes
    numSamples
    series_geo_accession
    series_status
    series_submission_date
    series_last_update_date
    series_pubmed_id
    series_type
    series_platform_id
    series_sample_taxid
    series_title""".split()
    print "\t".join(headers)

    for dirname in glob.glob("/Volumes/Archives/geo_mirror/DATA/SeriesMatrix/GSE*"):
        for filename in glob.glob("%s/*" % dirname):
            rec = getRec(filename)
            print "\t".join([str(rec[header]) for header in headers])



if __name__ == "__main__":
    print_GEO_summary()

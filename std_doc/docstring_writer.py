"""

PURPOSE
-------

Utility for automatically creating the framework for documenting python modules

CLASSES
-------

.. list-table::
  :header-rows: 1

  * - Class Name
    - Purpose
  * - _CodeSection
    - A section of code - intended superseded by inheriting classes
  * - ModuleToDoc
    - Class to write docstring for a module
  * - ClassToDoc
    - Class to write docstring for a class
  * - FnToDoc
    - Class to write docstring for a function

FUNCTIONS
---------

.. list-table::
  :header-rows: 1

  * - Function Name
    - Purpose
  * - main
    - External interface, allowing program to be run from command line, or executable file

"""

import argparse
import importlib.util
import inspect
from os.path import abspath
from re import search, compile, findall, sub


class _CodeSection:
    """

    PURPOSE
    -------

    A section of code - intended superseded by inheriting classes

    CLASSES
    -------

    .. list-table::
      :header-rows: 1

      * - Class Name
        - Purpose
      * - _CodeLine
        - A line of code in a section

    FUNCTIONS
    ---------

    .. list-table::
      :header-rows: 1

      * - Function Name
        - Purpose
      * - __init__
        - undocumented
      * - name
        - Dummy function - should be superseded by all inheriting classes
      * - kind
        - Dummy function - should be superseded by all inheriting classes
      * - purpose
        - Purpose documentation
      * - doc
        - Documentation for this section
      * - _standard_body_indentation
        - The standard indentation for the body of this section (i.e line 1 + \t, or line 2)
      * - exported
        - Flag for if the code section has been exported already
      * - _get_header
        - Dummy function - if subclass does not supersede, sets header to None
      * - _base_docs
        - Documentation for subclasses, functions, purpose, and any additional sections added by end user
      * - _doc_sect
        - Formats a section for the docstring with the correct title underline
      * - _f_line
        - Formatted line for output - typically for docstrings
      * - _find_docstr
        - Finds docstring
      * - _parse_docstr
        - Parses docstring to ensure no content is lost, and to identify all existing sections
      * - _split_code
        - Splits code by a keyword (def, class etc)
      * - _find_classes
        - Find sub-classes
      * - _find_fns
        - Finds sub functions
      * - export
        - Readies a code section for export

    """

    def __init__(self, section_as_text_l=None, section_as_code_l=None):
        """

        PARAMETERS
        ----------

        :param list[str]|None section_as_text_l:  File seperated into a list of lines
        :param list[_CodeSection._CodeLine]|None section_as_code_l:  Code as list of already instantiated objects

        """

        if section_as_text_l:
            self._body = [_CodeSection._CodeLine(text=line, owner=self) for line in section_as_text_l]
        else:
            self._body = section_as_code_l
            for line in self._body:
                line.belongs_to = self

        self._header = None
        self._get_header()

        self._docs = []
        self._classes = []
        self._fns = []

        self._find_docstr()
        self._find_classes()
        self._find_fns()

        self._docstr_data = {}
        self._parse_docstr()

        self._exported_status = False

    class _CodeLine:
        """

        PURPOSE
        -------

        A line of code in a section

        FUNCTIONS
        ---------

        .. list-table::
          :header-rows: 1

          * - Function Name
            - Purpose
          * - __init__
            - undocumented
          * - str_free
            - Line, stripped of any strings
          * - raw
            - Line as recorded from the original document
          * - marker
            - Flag of line type
          * - marker
            - Sets flag about line type
          * - indentation
            - Indentation of this line
          * - belongs_to
            - Code section that owns this line
          * - belongs_to
            - Set code section that owns this line

        """

        def __init__(self, text, owner):
            """

            PARAMETERS
            ----------

            :param str text:  text as recorded in the document
            :param _CodeSection owner:  The original owner for the line

            """

            self._text = text
            self._marker = "body"
            self._owner = owner

        @property
        def str_free(self):
            """

            PURPOSE
            -------

            Line, stripped of any strings

            PARAMETERS
            ----------

            :returns: Line of the document
            :rtype: str

            """

            if self.marker == "docs":
                return ""
            else:
                return sub(r"'.*'|\".*\"|\n", "", self._text)

        @property
        def raw(self):
            """

            PURPOSE
            -------

            Line as recorded from the original document

            PARAMETERS
            ----------

            :returns: Line of the document
            :rtype: str

            """

            return self._text

        @property
        def marker(self):
            """

            PURPOSE
            -------

            Flag of line type

            PARAMETERS
            ----------

            :returns: "header", "body" or "docs"
            :rtype: str

            """

            return self._marker

        @marker.setter
        def marker(self, new_marker):
            """

            PURPOSE
            -------

            Sets flag about line type

            PARAMETERS
            ----------

            :param str new_marker:  "header", "body" or "docs"

            """

            self._marker = new_marker

        @property
        def indentation(self):
            """

            PURPOSE
            -------

            Indentation of this line

            PARAMETERS
            ----------

            :returns: Whitespaces preceding the text
            :rtype: str

            """

            if search(r"^\s*", self._text).group():
                return search(r"^\s*", self._text).group()
            else:
                return ""

        @property
        def belongs_to(self):
            """

            PURPOSE
            -------

            Code section that owns this line

            PARAMETERS
            ----------

            :returns: Code section that owns this object
            :rtype: _CodeSection

            """

            return self._owner

        @belongs_to.setter
        def belongs_to(self, new_owner):
            """

            PURPOSE
            -------

            Set code section that owns this line

            PARAMETERS
            ----------

            :param _CodeSection new_owner:  owner of this line

            """

            self._owner = new_owner

    @property
    def name(self):
        """

        PURPOSE
        -------

        Dummy function - should be superseded by all inheriting classes

        PARAMETERS
        ----------

        :returns: "unknown"
        :rtype: str

        """

        return "unknown"

    @property
    def kind(self):
        """

        PURPOSE
        -------

        Dummy function - should be superseded by all inheriting classes

        PARAMETERS
        ----------

        :returns: "unknown"
        :rtype: str

        """

        return "unknown"

    @property
    def purpose(self):
        """

        PURPOSE
        -------

        Purpose documentation

        PARAMETERS
        ----------

        :returns: Just the purpose documentation for this section
        :rtype: str

        """

        if not self._docstr_data.get("PURPOSE"):
            return "undocumented"
        if "TODO:" not in self._docstr_data.get("PURPOSE"):
            return self._docstr_data.get("PURPOSE")
        else:
            return "undocumented"

    @property
    def doc(self):
        """

        PURPOSE
        -------

        Documentation for this section

        PARAMETERS
        ----------

        :returns: Documentation with sections PURPOSE, CLASSES, FUNCTIONS and any additional documentation
        :rtype: str

        """

        purpose_docs, sub_class_docs, sub_fn_docs, additional_docs = self._base_docs()
        return f"\n{purpose_docs}{sub_class_docs}{sub_fn_docs}{additional_docs}"

    @property
    def _standard_body_indentation(self):
        """

        PURPOSE
        -------

        The standard indentation for the body of this section (i.e. line 1 + \t, or line 2)

        PARAMETERS
        ----------

        :returns: whitespaces of the standard indentation
        :rtype: str

        """

        if self._header:
            return self._header.indentation + '    '
        else:
            return ""

    @property
    def exported(self):
        """

        PURPOSE
        -------

        Flag for if the code section has been exported already

        PARAMETERS
        ----------

        :returns: true if section has been exported
        :rtype: bool

        """

        return self._exported_status

    def _get_header(self):
        """

        PURPOSE
        -------

        Dummy function - if subclass does not supersede, sets header to None

        """

        self._header = None

    def _base_docs(self):
        """

        PURPOSE
        -------

        Documentation for subclasses, functions, purpose, and any additional sections added by end user

        PARAMETERS
        ----------

        :returns: purpose documentation, class documentation, fn documentation, additional documentation
        :rtype: tuple[str]

        """

        if self._classes:
            class_contents = (self._f_line(".. list-table::") + self._f_line("  :header-rows: 1") + '\n' +
                              self._f_line("  * - Class Name") + self._f_line("    - Purpose"))
            for class_ in self._classes:
                class_contents += self._f_line(f"  * - {class_.name}") + self._f_line(f"    - {class_.purpose}")

            class_docs = self._doc_sect("CLASSES", class_contents.strip())
        else:
            class_docs = ""

        if self._fns:
            fn_contents = (self._f_line(".. list-table::") + self._f_line("  :header-rows: 1") + '\n' +
                           self._f_line("  * - Function Name") + self._f_line("    - Purpose"))
            for fn in self._fns:
                fn_contents += self._f_line(f"  * - {fn.name}") + self._f_line(f"    - {fn.purpose}")
            fn_docs = self._doc_sect("FUNCTIONS", fn_contents.strip())
        else:
            fn_docs = ""

        additional_docs = ""
        for subheading, docs in {subheading: docs for subheading, docs in self._docstr_data.items()
                                 if subheading not in ["PURPOSE", "PARAMETERS", "EXCEPTIONS", "CLASSES",
                                                       "FUNCTIONS", "PARENT CLASS"]}.items():
            additional_docs += self._doc_sect(subheading, docs)

        if "PURPOSE" not in self._docstr_data.keys():
            purpose_docs = self._doc_sect("PURPOSE", f"TODO: Document purpose for {self.kind} {self.name}")
        else:
            purpose_docs = self._doc_sect("PURPOSE", self._docstr_data["PURPOSE"])

        return purpose_docs, class_docs, fn_docs, additional_docs

    def _doc_sect(self, heading, contents):
        """

        PURPOSE
        -------

        Formats a section for the docstring with the correct title underline

        PARAMETERS
        ----------

        :param str heading:  section header
        :param str contents:  section contents
        :returns: formatted section
        :rtype: str

        """

        indentation = self._standard_body_indentation
        return (f"{indentation}{heading}\n"
                + indentation + sub(r".", "-", heading)
                + f"\n\n{indentation}{contents}\n\n")

    def _f_line(self, contents):
        """

        PURPOSE
        -------

        Formatted line for output - typically for docstrings

        PARAMETERS
        ----------

        :param str contents:  text to format - should be stripped before passing in
        :returns: formatted line
        :rtype: str

        """

        return self._standard_body_indentation + contents + '\n'

    def _find_docstr(self):
        """

        PURPOSE
        -------

        Finds docstring

        """

        str_tracker = ""
        for line in self._body:
            if line.marker == "header":
                break
            str_tracker += line.raw
            if (len(findall("'''|\"\"\"", str_tracker)) % 2 != 0
                    or len(sub(r"'{3}.*'{3}|\"{3}.*\"{3}", "", line.raw).strip()) == 0
                    or len(sub(r"'{3}|\"{3}|\n", "", line.raw).strip()) == 0):
                line.marker = "docs"
                self._docs.append(line)
            else:
                pass
            if len(line.str_free.strip()) > 0:
                break
        self._body = [i for i in self._body if i not in self._docs]
        pass

    def _parse_docstr(self):
        """

        PURPOSE
        -------

        Parses docstring to ensure no content is lost, and to identify all existing sections

        """

        subheader_underline = compile(r"(?<!\S)(-+)$")
        last_i = len(self._docs)
        for i in range(len(self._docs) - 2, -1, -1):
            if search(subheader_underline, self._docs[i + 1].raw.strip()):
                self._docstr_data[self._docs[i].raw.strip()] = ""
                for line in self._docs[i + 2: last_i]:
                    self._docstr_data[self._docs[i].raw.strip()] += line.raw
                last_i = i
            elif i == 0:
                if not self._docstr_data.get("TEMP NOTES"):
                    self._docstr_data["TEMP NOTES"] = ""
                else:
                    self._docstr_data["TEMP NOTES"] = sub("TODO: move these notes into a section with a header\n", "",
                                                          self._docstr_data["TEMP NOTES"])
                for line in self._docs[i: last_i]:
                    self._docstr_data["TEMP NOTES"] += line.raw

        for key, docs in self._docstr_data.items():
            self._docstr_data[key] = sub(r"\"{3}|\'{3}", "", docs).strip()

        if self._docstr_data.get("TEMP NOTES"):
            self._docstr_data["TEMP NOTES"] = ("TODO: move these notes into a section with a header\n"
                                               + self._docs[0].indentation
                                               + self._docstr_data["TEMP NOTES"].strip())
        else:
            self._docstr_data = {sect: self._docstr_data[sect] for sect in
                                 self._docstr_data.keys() - {"TEMP NOTES"}}

    def _split_code(self, search_term):
        """

        PURPOSE
        -------

        Splits code by a keyword (def, class etc)

        PARAMETERS
        ----------

        :param re.Pattern search_term:  keyword to split code by
        :returns: Split code
        :rtype: list[list[_CodeSection._CodeLine]]

        """

        split_code = [[]]
        block_indentation = self._standard_body_indentation

        for i in self._body:
            if i.indentation == block_indentation:
                split_code.append([i])
            elif len(i.indentation) > len(block_indentation) or len(i.str_free) == 0:
                split_code[-1].append(i)

        split_code = [i for i in split_code if i]

        return [block for block in split_code if search(search_term, block[0].str_free)]

    def _find_classes(self):
        """

        PURPOSE
        -------

        Find sub-classes

        """

        class_set = self._split_code(search_term=compile(r"\bclass\s"))
        self._classes = [ClassToDoc(code=class_code) for class_code in class_set]

    def _find_fns(self):
        """

        PURPOSE
        -------

        Finds sub functions

        """

        fn_set = self._split_code(search_term=compile(r"\bdef\s"))
        self._fns = [FnToDoc(code=fn_code) for fn_code in fn_set]

    def export(self):
        """

        PURPOSE
        -------

        Readies a code section for export

        PARAMETERS
        ----------

        :returns: documentation and section code
        :rtype: str

        """

        to_export = ''
        self._exported_status = True
        if self._header:
            to_export += self._header.raw
        to_export += (self._standard_body_indentation + "\"\"\"\n" +
                      self.doc + self._standard_body_indentation + "\"\"\"\n\n")
        for line in self._body:
            if line.belongs_to.exported is False:
                to_export += line.belongs_to.export()
            elif line.belongs_to is self:
                to_export += line.raw
        return to_export


class ModuleToDoc(_CodeSection):
    """

    PURPOSE
    -------

    Class to write docstring for a module

    PARENT CLASS
    ------------

    _CodeSection

    FUNCTIONS
    ---------

    .. list-table::
      :header-rows: 1

      * - Function Name
        - Purpose
      * - __init__
        - undocumented
      * - name
        - Name of the module (file name)
      * - kind
        - Returns "module"
      * - export
        - Rewrite the file with the docstring changes

    PARENT CLASS
    ------------

    _CodeSection

    """

    def __init__(self, filepath: str):
        """

        PARAMETERS
        ----------

        :param str filepath:  filepath for module to document

        """

        module_spec = importlib.util.spec_from_file_location("module_obj", filepath)
        module_obj = importlib.util.module_from_spec(module_spec)
        super().__init__(section_as_text_l=inspect.getsourcelines(module_obj)[0])
        self._file_path = filepath
        self._file_name = filepath.rsplit('\\', 1)[1]

    @property
    def name(self):
        """

        PURPOSE
        -------

        Name of the module (file name)

        PARAMETERS
        ----------

        :returns: module name
        :rtype: str

        """

        return self._file_name

    @property
    def kind(self):
        """

        PURPOSE
        -------

        Returns "module"

        PARAMETERS
        ----------

        :returns: "module"
        :rtype: str

        """

        return "module"

    def export(self):
        """

        PURPOSE
        -------

        Rewrite the file with the docstring changes

        """

        contents = super(ModuleToDoc, self).export()
        with open(self._file_path, 'w') as f:
            f.write(contents)


class ClassToDoc(_CodeSection):
    """

    PURPOSE
    -------

    Class to write docstring for a class

    PARENT CLASS
    ------------

    _CodeSection

    FUNCTIONS
    ---------

    .. list-table::
      :header-rows: 1

      * - Function Name
        - Purpose
      * - __init__
        - undocumented
      * - name
        - Class name
      * - inherited_from
        - Parent class
      * - kind
        - returns "class"
      * - doc
        - Documentation for the class
      * - _get_header
        - Flags first line of class (class class_name():)

    PARENT CLASS
    ------------

    _CodeSection

    """

    def __init__(self, code):
        """

        PARAMETERS
        ----------

        :param list[_CodeSection._CodeLine] code:  lines of code in class

        """

        super().__init__(section_as_code_l=code)

    @property
    def name(self):
        """

        PURPOSE
        -------

        Class name

        PARAMETERS
        ----------

        :returns: class name
        :rtype: str

        """

        return search(r"(?<=\bclass\s)\w*", self._header.raw).group()

    @property
    def inherited_from(self):
        """

        PURPOSE
        -------

        Parent class

        PARAMETERS
        ----------

        :returns: parent class name
        :rtype: str

        """

        if search(r"\(.*\)", self._header.raw):
            return search(r"(?<=\().*(?=\))", self._header.raw).group()
        else:
            return None

    @property
    def kind(self):
        """

        PURPOSE
        -------

        returns "class"

        PARAMETERS
        ----------

        :returns: "class"
        :rtype: str

        """

        return "class"

    @property
    def doc(self):
        """

        PURPOSE
        -------

        Documentation for the class

        PARAMETERS
        ----------

        :returns: Documentation with sections PURPOSE, PARENT CLASS (if applicable), CLASSES, FUNCTIONS
        :rtype: str

        """

        purpose_docs, sub_class_docs, sub_fn_docs, additional_docs = self._base_docs()
        if self.inherited_from:
            parent_docs = self._doc_sect("PARENT CLASS", self.inherited_from)
        else:
            parent_docs = ""

        return f"\n{purpose_docs}{parent_docs}{sub_class_docs}{sub_fn_docs}{additional_docs}"

    def _get_header(self):
        """

        PURPOSE
        -------

        Flags first line of class (class class_name():)

        """

        if search(r"\bclass\s", self._body[0].str_free):
            self._body[0].marker = "header"
            self._header = self._body.pop(0)
        else:
            self._header = None


class FnToDoc(_CodeSection):
    """

    PURPOSE
    -------

    Class to write docstring for a function

    PARENT CLASS
    ------------

    _CodeSection

    CLASSES
    -------

    .. list-table::
      :header-rows: 1

      * - Class Name
        - Purpose
      * - _Parameter
        - A parameter for a function

    FUNCTIONS
    ---------

    .. list-table::
      :header-rows: 1

      * - Function Name
        - Purpose
      * - __init__
        - undocumented
      * - name
        - Name of the function
      * - kind
        - returns 'function'
      * - doc
        - Documentation for the function
      * - _param_names
        - Names of the function parameters
      * - _find_parameters
        - Finds parameters by looking at code body - also searches for indications of a return, and any raised
        exceptions
      * - _parse_docstr
        - Parse function docstring for parameters, and return type/details
      * - _get_header
        - Flags first line of function (def fn_name():)

    PARENT CLASS
    ------------

    _CodeSection

    """

    def __init__(self, code):
        """

        PARAMETERS
        ----------

        :param list[_CodeSection._CodeLine] code:  lines of code in function

        """

        self._parameters = []
        self._exceptions = []
        self._has_return = False
        self._returns = None
        self._rtype = None
        super().__init__(section_as_code_l=code)
        self._find_parameters()

    @property
    def name(self):
        """

        PURPOSE
        -------

        Name of the function

        PARAMETERS
        ----------

        :returns: function name
        :rtype: str

        """

        return search(r"(?<=\bdef\s)\w*", self._header.raw).group()

    @property
    def kind(self):
        """

        PURPOSE
        -------

        returns 'function'

        PARAMETERS
        ----------

        :returns: 'function'
        :rtype: str

        """

        return "function"

    @property
    def doc(self):
        """

        PURPOSE
        -------

        Documentation for the function

        PARAMETERS
        ----------

        :returns: Documentation with sections PURPOSE (unless __init__) and PARAMETERS, CLASSES, FUNCTIONS and
        :rtype: str

        """

        purpose_docs, sub_class_docs, sub_fn_docs, additional_docs = self._base_docs()

        if self.name == "__init__":
            purpose_docs = ""

        param_contents = ""
        self._parameters = [p for p in self._parameters if p.name != 'TODO']
        for param in self._parameters:
            param_contents += self._f_line(param.doc)

        if self._has_return:
            if not self._returns and self._rtype != "None":
                param_contents += self._f_line(f":returns: TODO: Document the return for function {self.name}")
            else:
                param_contents += self._f_line(":returns: " + self._returns)

            if not self._rtype:
                param_contents += self._f_line(f":rtype: TODO: Document return type for function {self.name}")
            else:
                param_contents += self._f_line(":rtype: " + self._rtype)

        if param_contents != "":
            param_docs = self._doc_sect("PARAMETERS", param_contents.strip())
        else:
            param_docs = ""

        exception_docs = ""
        if self._exceptions:
            exception_contents = ""
            for ex in self._exceptions:
                exception_contents += self._f_line(ex)
            exception_docs = self._doc_sect("EXCEPTIONS", exception_contents.strip())

        return f"\n{purpose_docs}{param_docs}{exception_docs}{sub_class_docs}{sub_fn_docs}{additional_docs}"

    @property
    def _param_names(self):
        """

        PURPOSE
        -------

        Names of the function parameters

        PARAMETERS
        ----------

        :returns: List of parameter names
        :rtype: list[str]

        """

        return [param.name for param in self._parameters]

    def _find_parameters(self):
        """

        PURPOSE
        -------

        Finds parameters by looking at code body - also searches for indications of a return, and any raised exceptions

        """

        inputs = search(r"(?<=\().*(?=\))", self._header.raw).group()
        for param in inputs.split(","):
            p_details = search(r"(\w+)\s?:?\s?(.*)?", param)
            if p_details.group(1) == "self" or p_details.group(1) == "cls" or p_details.group(1) in self._param_names:
                continue
            self._parameters.append(FnToDoc._Parameter(name=p_details.group(1), p_type=p_details.group(2), desc=None))
        if search(r"(?<=\) ->).*(?=:)", self._header.str_free):
            self._rtype = search(r"(?<=->).*(?=:)", self._header.str_free).group().strip()
        for line in self._body:
            if search(r"\braise\b", line.str_free):
                self._exceptions.append(search(r"(?<=\braise\s).*", line.raw).group().strip())
            if search(r"\breturn\b", line.str_free):
                if len(sub(r"\breturn\b", "", line.raw).strip()) > 0:
                    self._has_return = True

    def _parse_docstr(self):
        """

        PURPOSE
        -------

        Parse function docstring for parameters, and return type/details

        """

        super(FnToDoc, self)._parse_docstr()
        for docs in self._docstr_data.values():
            for line in docs.split('\n'):
                if search(r":param .*:", line):
                    p_details = search(r"(?<=:param)\s?(.+)?\s(\w+):(.+)?", line)
                    self._parameters.append(FnToDoc._Parameter(name=p_details.group(2),
                                                               p_type=p_details.group(1),
                                                               desc=p_details.group(3)))
                if search(r":returns?:", line):
                    self._has_return = True
                    self._returns = sub(r":returns?:", "", line).strip()
                if search(r":rtype:", line):
                    self._has_return = True
                    self._rtype = sub(r":rtype:", "", line).strip()

    def _get_header(self):
        """

        PURPOSE
        -------

        Flags first line of function (def fn_name():)

        """

        if search(r"\bdef\s", self._body[0].str_free):
            self._body[0].marker = "header"
            self._header = self._body.pop(0)
        else:
            self._header = None

    class _Parameter:
        """

        PURPOSE
        -------

        A parameter for a function

        FUNCTIONS
        ---------

        .. list-table::
          :header-rows: 1

          * - Function Name
            - Purpose
          * - __init__
            - undocumented
          * - name
            - Name of parameter
          * - doc
            - Documents parameter

        """

        def __init__(self, name, p_type, desc):
            """

            PARAMETERS
            ----------

            :param str name:  name of the parameter
            :param str|None p_type: parameter type (eg str, int etc.)
            :param str|None desc: short description of the parameter

            """

            self._name = name.strip()
            self._type = p_type
            self._desc = desc

        @property
        def name(self):
            """

            PURPOSE
            -------

            Name of parameter

            PARAMETERS
            ----------

            :returns: parameter name
            :rtype: str

            """

            return self._name

        @property
        def doc(self):
            """

            PURPOSE
            -------

            Documents parameter

            PARAMETERS
            ----------

            :returns: {description}
            :rtype: str

            """

            if not self._desc and not self._type:
                self._desc = f"TODO: document description and type for parameter {self._name}"
            elif not self._desc:
                self._desc = f"TODO: document description for parameter {self._name}"
            elif not self._type or self._type == "None":
                self._desc += f" TODO: document type for parameter {self._name}"
            return f":param {self._type.strip()} {self._name}: {self._desc.strip()}"


def main():
    """

    PURPOSE
    -------

    External interface, allowing program to be run from command line, or executable file

    """

    parser = argparse.ArgumentParser(description="Utility for automatically creating and maintaining the framework "
                                                 "for documenting Python modules")

    parser.add_argument("-f", "--filepath", type=str, nargs=1,
                        metavar="file_path", default=None,
                        help="The file to write docstrings for - either relative to current location, or absolute")

    args = parser.parse_args()

    if args.filepath is not None:
        ModuleToDoc(abspath(args.filepath[0])).export()


if __name__ == "__main__":
    main()

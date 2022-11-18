"""

PURPOSE
-------

TODO: Document purpose for module docstring_test_file.py

CLASSES
-------

.. list-table::
  :header-rows: 1

  * - Class Name
    - Purpose
  * - _CodeSection
    - undocumented
  * - ModuleToDoc
    - undocumented
  * - ClassToDoc
    - undocumented
  * - FnToDoc
    - undocumented

FUNCTIONS
---------

.. list-table::
  :header-rows: 1

  * - Function Name
    - Purpose
  * - main
    - undocumented

"""

import argparse
import importlib.util
import inspect
from os.path import abspath
from re import search, compile, findall, sub
import sys


class _CodeSection:
    """

    PURPOSE
    -------

    TODO: Document purpose for class _CodeSection

    CLASSES
    -------

    .. list-table::
      :header-rows: 1

      * - Class Name
        - Purpose
      * - _CodeLine
        - undocumented

    FUNCTIONS
    ---------

    .. list-table::
      :header-rows: 1

      * - Function Name
        - Purpose
      * - __init__
        - undocumented
      * - name
        - undocumented
      * - kind
        - undocumented
      * - purpose
        - undocumented
      * - doc
        - undocumented
      * - _standard_body_indentation
        - undocumented
      * - exported
        - undocumented
      * - _get_header
        - undocumented
      * - _base_docs
        - undocumented
      * - _doc_sect
        - undocumented
      * - _f_line
        - undocumented
      * - _find_docstr
        - undocumented
      * - _parse_docstr
        - undocumented
      * - _split_code
        - undocumented
      * - _find_classes
        - undocumented
      * - _find_fns
        - undocumented
      * - export
        - undocumented

    """

    def __init__(self, section_as_text_l=None, section_as_code_l=None):
        """

        PARAMETERS
        ----------

        :param =None section_as_text_l: TODO: document description for parameter section_as_text_l
        :param =None section_as_code_l: TODO: document description for parameter section_as_code_l

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

        TODO: Document purpose for class _CodeLine

        FUNCTIONS
        ---------

        .. list-table::
          :header-rows: 1

          * - Function Name
            - Purpose
          * - __init__
            - undocumented
          * - str_free
            - undocumented
          * - raw
            - undocumented
          * - marker
            - undocumented
          * - marker
            - undocumented
          * - indentation
            - undocumented
          * - belongs_to
            - undocumented
          * - belongs_to
            - undocumented

        """

        def __init__(self, text, owner):
            """

            PARAMETERS
            ----------

            :param  text: TODO: document description and type for parameter text
            :param  owner: TODO: document description and type for parameter owner

            """

            self._text = text
            self._marker = "body"
            self._owner = owner

        @property
        def str_free(self):
            """

            PURPOSE
            -------

            TODO: Document purpose for function str_free

            PARAMETERS
            ----------

            :returns: TODO: Document the return for function str_free
            :rtype: TODO: Document return type for function str_free

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

            TODO: Document purpose for function raw

            PARAMETERS
            ----------

            :returns: TODO: Document the return for function raw
            :rtype: TODO: Document return type for function raw

            """

            return self._text

        @property
        def marker(self):
            """

            PURPOSE
            -------

            TODO: Document purpose for function marker

            PARAMETERS
            ----------

            :returns: TODO: Document the return for function marker
            :rtype: TODO: Document return type for function marker

            """

            return self._marker

        @marker.setter
        def marker(self, new_marker):
            """

            PURPOSE
            -------

            TODO: Document purpose for function marker

            PARAMETERS
            ----------

            :param  new_marker: TODO: document description and type for parameter new_marker

            """

            self._marker = new_marker

        @property
        def indentation(self):
            """

            PURPOSE
            -------

            TODO: Document purpose for function indentation

            PARAMETERS
            ----------

            :returns: TODO: Document the return for function indentation
            :rtype: TODO: Document return type for function indentation

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

            TODO: Document purpose for function belongs_to

            PARAMETERS
            ----------

            :returns: TODO: Document the return for function belongs_to
            :rtype: TODO: Document return type for function belongs_to

            """

            return self._owner

        @belongs_to.setter
        def belongs_to(self, new_owner):
            """

            PURPOSE
            -------

            TODO: Document purpose for function belongs_to

            PARAMETERS
            ----------

            :param  new_owner: TODO: document description and type for parameter new_owner

            """

            self._owner = new_owner

    @property
    def name(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function name

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function name
        :rtype: TODO: Document return type for function name

        """

        return "unknown"

    @property
    def kind(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function kind

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function kind
        :rtype: TODO: Document return type for function kind

        """

        return "unknown"

    @property
    def purpose(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function purpose

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function purpose
        :rtype: TODO: Document return type for function purpose

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

        TODO: Document purpose for function doc

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function doc
        :rtype: TODO: Document return type for function doc

        """

        purpose_docs, sub_class_docs, sub_fn_docs, additional_docs = self._base_docs()
        return f"\n{purpose_docs}{sub_class_docs}{sub_fn_docs}{additional_docs}"

    @property
    def _standard_body_indentation(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function _standard_body_indentation

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function _standard_body_indentation
        :rtype: TODO: Document return type for function _standard_body_indentation

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

        TODO: Document purpose for function exported

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function exported
        :rtype: TODO: Document return type for function exported

        """

        return self._exported_status

    def _get_header(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function _get_header

        """

        self._header = None

    def _base_docs(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function _base_docs

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function _base_docs
        :rtype: TODO: Document return type for function _base_docs

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
                                 if subheading not in ["PURPOSE", "PARAMETERS",
                                                       "EXCEPTIONS", "CLASSES", "FUNCTIONS"]}.items():
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

        TODO: Document purpose for function _doc_sect

        PARAMETERS
        ----------

        :param  heading: TODO: document description and type for parameter heading
        :param  contents: TODO: document description and type for parameter contents
        :returns: TODO: Document the return for function _doc_sect
        :rtype: TODO: Document return type for function _doc_sect

        """

        indentation = self._standard_body_indentation
        return (f"{indentation}{heading}\n"
                + indentation + sub(r".", "-", heading)
                + f"\n\n{indentation}{contents}\n\n")

    def _f_line(self, contents):
        """

        PURPOSE
        -------

        TODO: Document purpose for function _f_line

        PARAMETERS
        ----------

        :param  contents: TODO: document description and type for parameter contents
        :returns: TODO: Document the return for function _f_line
        :rtype: TODO: Document return type for function _f_line

        """

        return self._standard_body_indentation + contents + '\n'

    def _find_docstr(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function _find_docstr

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

        TODO: Document purpose for function _parse_docstr

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
                self._docstr_data["TEMP NOTES"] = ""
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

        TODO: Document purpose for function _split_code

        PARAMETERS
        ----------

        :param  search_term: TODO: document description and type for parameter search_term
        :returns: TODO: Document the return for function _split_code
        :rtype: TODO: Document return type for function _split_code

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

        TODO: Document purpose for function _find_classes

        """

        class_set = self._split_code(search_term=compile(r"\bclass\s"))
        self._classes = [ClassToDoc(code=class_code) for class_code in class_set]

    def _find_fns(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function _find_fns

        """

        fn_set = self._split_code(search_term=compile(r"\bdef\s"))
        self._fns = [FnToDoc(code=fn_code) for fn_code in fn_set]

    def export(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function export

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function export
        :rtype: TODO: Document return type for function export

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

    TODO: Document purpose for class ModuleToDoc

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
        - undocumented
      * - kind
        - undocumented
      * - export
        - undocumented

    TEMP NOTES
    ----------

    TODO: move these notes into a section with a header
    Class to write docstring for a module

    """

    def __init__(self, filepath: str):
        """

        PARAMETERS
        ----------

        :param str filepath: TODO: document description for parameter filepath

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

        TODO: Document purpose for function name

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function name
        :rtype: TODO: Document return type for function name

        """

        return self._file_name

    @property
    def kind(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function kind

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function kind
        :rtype: TODO: Document return type for function kind

        """

        return "module"

    def export(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function export

        """

        contents = super(ModuleToDoc, self).export()
        with open(self._file_path, 'w') as f:
            f.write(contents)


class ClassToDoc(_CodeSection):
    """

    PURPOSE
    -------

    TODO: Document purpose for class ClassToDoc

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
        - undocumented
      * - inherited_from
        - undocumented
      * - kind
        - undocumented
      * - doc
        - undocumented
      * - _get_header
        - undocumented

    TEMP NOTES
    ----------

    TODO: move these notes into a section with a header
    Class to write docstring for a class

    """

    def __init__(self, code):
        """

        PARAMETERS
        ----------

        :param  code: TODO: document description and type for parameter code

        """

        super().__init__(section_as_code_l=code)

    @property
    def name(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function name

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function name
        :rtype: TODO: Document return type for function name

        """

        return search(r"(?<=\bclass\s)\w*", self._header.raw).group()

    @property
    def inherited_from(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function inherited_from

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function inherited_from
        :rtype: TODO: Document return type for function inherited_from

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

        TODO: Document purpose for function kind

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function kind
        :rtype: TODO: Document return type for function kind

        """

        return "class"

    @property
    def doc(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function doc

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function doc
        :rtype: TODO: Document return type for function doc

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

        TODO: Document purpose for function _get_header

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

    TODO: Document purpose for class FnToDoc

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
        - undocumented

    FUNCTIONS
    ---------

    .. list-table::
      :header-rows: 1

      * - Function Name
        - Purpose
      * - __init__
        - undocumented
      * - name
        - undocumented
      * - kind
        - undocumented
      * - doc
        - undocumented
      * - _param_names
        - undocumented
      * - _find_parameters
        - undocumented
      * - _parse_docstr
        - undocumented
      * - _get_header
        - undocumented

    TEMP NOTES
    ----------

    TODO: move these notes into a section with a header
    Class to write docstring for a function

    """

    def __init__(self, code):
        """

        PARAMETERS
        ----------

        :param  code: TODO: document description and type for parameter code

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

        TODO: Document purpose for function name

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function name
        :rtype: TODO: Document return type for function name

        """

        return search(r"(?<=\bdef\s)\w*", self._header.raw).group()

    @property
    def kind(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function kind

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function kind
        :rtype: TODO: Document return type for function kind

        """

        return "function"

    @property
    def doc(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function doc

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function doc
        :rtype: TODO: Document return type for function doc

        """

        purpose_docs, sub_class_docs, sub_fn_docs, additional_docs = self._base_docs()

        if self.name == "__init__":
            purpose_docs = ""

        param_contents = ""
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

        TODO: Document purpose for function _param_names

        PARAMETERS
        ----------

        :returns: TODO: Document the return for function _param_names
        :rtype: TODO: Document return type for function _param_names

        """

        return [param.name for param in self._parameters]

    def _find_parameters(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function _find_parameters

        """

        inputs = search(r"(?<=\().*(?=\))", self._header.raw).group()
        for param in inputs.split(","):
            p_details = search(r"(\w+)\s?:?\s?(.*)?", param)
            if p_details.group(1) == "self" or p_details.group(1) in self._param_names:
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

        TODO: Document purpose for function _parse_docstr

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
                    self._returns = sub(r":.*:", "", line).strip()
                if search(r":rtype:", line):
                    self._has_return = True
                    self._rtype = sub(r":.*:", "", line).strip()

    def _get_header(self):
        """

        PURPOSE
        -------

        TODO: Document purpose for function _get_header

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

        TODO: Document purpose for class _Parameter

        FUNCTIONS
        ---------

        .. list-table::
          :header-rows: 1

          * - Function Name
            - Purpose
          * - __init__
            - undocumented
          * - name
            - undocumented
          * - doc
            - undocumented

        """

        def __init__(self, name, p_type, desc):
            """

            PARAMETERS
            ----------

            :param  name: TODO: document description and type for parameter name
            :param  p_type: TODO: document description and type for parameter p_type
            :param  desc: TODO: document description and type for parameter desc

            """

            self._name = name.strip()
            self._type = p_type
            self._desc = desc

        @property
        def name(self):
            """

            PURPOSE
            -------

            TODO: Document purpose for function name

            PARAMETERS
            ----------

            :returns: TODO: Document the return for function name
            :rtype: TODO: Document return type for function name

            """

            return self._name

        @property
        def doc(self):
            """

            PURPOSE
            -------

            TODO: Document purpose for function doc

            PARAMETERS
            ----------

            :returns: TODO: Document the return for function doc
            :rtype: TODO: Document return type for function doc

            """

            if not self._desc and not self._type:
                self._desc = f"TODO: document description and type for parameter {self._name}"
            elif not self._desc:
                self._desc = f"TODO: document description for parameter {self._name}"
            elif not self._type or self._type == "None":
                self._desc += f" TODO: document type for parameter {self._name}"
            return f":param {self._type} {self._name}: {self._desc}"


def main():
    """

    PURPOSE
    -------

    TODO: Document purpose for function main

    """

    parser = argparse.ArgumentParser(description="script to automatically write docstrings for modules and classes")

    parser.add_argument("-f", "--filepath", type=str, nargs=1,
                        metavar="file_path", default=None,
                        help="The file to write docstrings for")

    args = parser.parse_args()

    if args.filepath is not None:
        ModuleToDoc(abspath(args.filepath[0])).export()
    elif sys.argv:
        for filepath in sys.argv:
            ModuleToDoc(abspath(filepath))


if __name__ == "__main__":
    main()

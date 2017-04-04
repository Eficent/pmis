# -*- coding: utf-8 -*-
# © 2014-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Progress measurement",
    "version": "9.0.1.0.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules",
    "depends": ["project"],
    "description": """
Progress measurement
====================================
    The progress of a project indicates the degree of completion, with respect to the estimated scope of work.
    Generally the progress cannot be automatically measured and it is based on the expert judgement or the
    completion of checklists that determine the degree of completion of a project.


Define Progress Types:
------------------------------------
    Each company can have different needs of project progress control.
    It is for this reason that it is necessary to define Progress Types.
    The Progress Types are entities that can be created to measure the progress differently.
    For example, a project can be measured on a percent basis, or by quantity used of a given resource.
    A Progress Type is defined by the following attributes:
        * Name: Name given to the type of progress
        * Maximum value: Maximum value that is permitted for the object being measured as a total measure of progress.
        * Precision: Value of increments permitted for the given progress type measured as a total measure of progress.


Define Progress Measurements:
------------------------------------
    Progress Measurements record the results of the measurement.
    A Progress Measurement is defined by the following attributes:
        * Date: When the measurement occurred
        * Progress Type.
        * Value: Results of the measurement. Must be defined in the precision indicated by the progress type.
        The user cannot enter a value that exceeds the maximum permitted value for that progress type.
        * Description: description of the measurement
        * Entered by: User that entered the measurement
    """,
    "data": [
        "views/progress_measurement_type_view.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True,
    'application': False,
}

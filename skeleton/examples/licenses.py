"""
Skeletons for BSD, GPL and LGPL licenses.
"""

from skeleton import Skeleton, Var


BSD_THIRD_CLAUSE = """
    - Neither the name of the {Organization} nor the names of its contributors 
      may be used to endorse or promote products derived from this software 
      without specific prior written permission.
"""


class NoLicense(Skeleton):
    """
    Had the a license with copyright notice only.
    """
    src = 'licenses/no-license'
    vars = [ Var('Author') ]


class BSD(Skeleton):
    """
    Adds a 2 or 3 clauses BSD License.
    
    Requires Author and Organization variables.
    
    Sets a ThirdClause variable.
    """

    src = 'licenses/bsd'
    vars = [
        Var('Author'),
        Var('Organization',
            default='',
            description="required for a 3 clauses-BSD license - "
                "leave it empty for a 2 clauses-BSD license."
            ),
        ]

    def write(self, dst_dir):
        """
        Set the ThirdClause if an organization name has been given.
        """
        if self.get('Organization'):
            self['ThirdClause'] = self.template_formatter(BSD_THIRD_CLAUSE)
        else:
            self['ThirdClause'] = ''
        super(BSD, self).write(dst_dir)


class GPL(Skeleton):
    """
    Adds a GPL notice and the GPLv3 license.
    
    Requires Author and ProjectName variables.
    """

    src = 'licenses/gpl'
    vars = [
        Var('Author'),
        Var('ProjectName'),
        ]


class LGPL(GPL):
    """
    Add a LGPL Notice and the GPLv3 and LGPLv3 licenses
    
    Requires Author and ProjectName variables.
    """
    src = 'licenses/lgpl'

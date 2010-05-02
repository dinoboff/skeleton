"""
Skeletons for BSD, GPL and LGPL licenses.
"""

from skeleton import Skeleton, Var


BSD_THIRD_CLAUSE = """
    - Neither the name of the {Organization} nor the names of its contributors 
      may be used to endorse or promote products derived from this software 
      without specific prior written permission.
"""


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

    def pre_write(self, *args, **kw):
        """
        Set the ThirdClause if an organization name has been given.
        """
        if self.get('Organization'):
            self['ThirdClause'] = self.template_formatter(BSD_THIRD_CLAUSE)
        else:
            self['ThirdClause'] = ''

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProjectSyusro(models.Model):
    _name = 'project.syusro'
    _description = 'Gestión de SYUSRO (Usuarios para Proyectos)'

    syusro_cd = fields.Integer(string="Código", required=True)
    syusro_nm = fields.Char(string="Nombre", required=True)
    syusro_rol = fields.Char(string="Rol")
    syusro_fc_alta = fields.Date(string="Fecha de Alta")
    syusro_estado = fields.Selection([
            ('HABI','Activo'),
            ('INHA','Inactivo')
        ],
        string = "Estado"
    )

    # Campo computado que conecta con todos los empleados (hr.employee)
    employee_ids = fields.Many2many(
        'hr.employee',
        string="Empleados",
        compute="_compute_employee_ids",
        store=False,
        help="Empleados de todas las compañías relacionados con este Syusro"
    )

    ##################################################################################################################
    #Compute's
    ##################################################################################################################

    def _compute_display_name(self):
        for record in self:
            if record.syusro_cd:
                record.display_name = f"[{record.syusro_cd}] {record.syusro_nm}"
            else:
                record.display_name = record.syusro_nm

    
    @api.depends('syusro_cd')
    def _compute_employee_ids(self):
        for rec in self:
            # Se utiliza sudo() para evitar restricciones por compañía.
            # Aquí se busca por nombre; si tienes un campo en hr.employee que
            # almacene el código o referencia, puedes ajustar el dominio.
            rec.employee_ids = self.env['hr.employee'].sudo().search([
                ('x_studio_nv_numero_de_legajo', '=', rec.syusro_cd)
            ])

    ##################################################################################################################
    #Restricciones
    ##################################################################################################################
    
    _sql_constraints = [
        ('syusro_cd_unique', 'unique(syusro_cd)', 'El código debe ser único.')
    ]

    ##################################################################################################################
    #Funciones base de odoo
    ##################################################################################################################

    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', limit=100, order=None, name_get_uid=None):
        """Búsqueda por 'name' o 'code' en campos Many2one."""

        if domain is None:  
            domain = []  # Si domain es None, lo inicializamos como una lista vacía
        
        if name:
            # Agregar condiciones de búsqueda (obra_nr o name)
            domain = ['&', '|', ('syusro_cd', operator, name), ('syusro_nm', operator, name), ('syusro_estado', '=', 'HABI')] + domain
            #domain = ['|', ('syusro_cd', operator, name), ('syusro_nm', operator, name)] + domain
            
        #_logger.warning(f"*****************************  _name_search ****************************")
        #_logger.warning(f"name: {syusro_nm} \ndomain {domain} \noperator: {operator} \nlimit: {limit} \norder: {order} \nname_get_uid: {name_get_uid}")
        rtn = self._search(domain, limit=limit, order=order)
        #_logger.warning(f"rtn: {rtn}")
        return rtn



    






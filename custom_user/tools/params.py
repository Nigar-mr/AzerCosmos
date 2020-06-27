from drf_yasg import openapi

auth_header = openapi.Parameter('Authorization',
                                openapi.IN_HEADER,
                                description="Token [code]",
                                type=openapi.TYPE_STRING,
                                required=True)

query = openapi.Parameter('q',
                          openapi.IN_QUERY,
                          description="Search params to country",
                          type=openapi.TYPE_STRING,
                          required=False)

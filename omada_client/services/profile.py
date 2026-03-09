from omada_client.core.base_service import BaseService
from omada_client.types.models import ProfileGroupModel
from omada_client.types.responses import ComplexResponseGeneric


class ProfileGroup(BaseService):

    def get_all_group(self) -> list[ProfileGroupModel] | None:
        self.client.Check.site()

        response_model: ComplexResponseGeneric[list[ProfileGroupModel]] = self.request.GET(
            path=f"sites/{self.client.site_id}/profiles/groups",
            model=ComplexResponseGeneric[list[ProfileGroupModel]]
        )

        return response_model.result

    def get_group_by_id(self, group_id:str) -> ProfileGroupModel | None:
        response = self.get_all_group()

        if response:
            all_group:list[ProfileGroupModel] = response
            
            for group in all_group:
                if group.group_id == group_id:
                    return group

        return None
    
    def get_group_by_name(self, group_name:str) -> ProfileGroupModel | None:
        response = self.get_all_group()

        if response:
            all_group:list[ProfileGroupModel] = response
            
            for group in all_group:
                if group.name == group_name:
                    return group

        return None
    
    # TO-DO
    # def create_group(self, group: dict[str, Any]) -> ProfileGroupModel | None:
    #     self.client.Check.site()
    #     group_valid = ProfileGroupModel.model_validate(group)

    #     response_model: ComplexResponseGeneric[IdResponseModel] = self.request.POST(
    #         path=f"sites/{self.client.site_id}/profiles/groups",
    #         data=group_valid.model_dump(),
    #         model=ComplexResponseGeneric[IdResponseModel]
    #     )
        
    #     if response_model.result and response_model.result.id:
    #         return self.get_group_by_id(response_model.result.id)

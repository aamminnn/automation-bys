require 'pre_receive_hooks_spec_helper'
require 'pry'

feature "Pre-receive hooks" do
  before(:all) do
    @user = get_admin_user(:login)
    @password = get_admin_user(:password)
    @timestamp = ENV['TS'] || new_timestamp
    @repo_name = "sanity-test-#{@timestamp}"

    @client = Octokit::Client.new(login: @user, password: @password)
    @client.connection_options[:ssl] = { verify: false }

    add_ssh_keys_to_user_account
  end

  before(:each) do
    login
  end

  after(:all) do
    remove_ssh_keys_from_user_account
  end

  let(:prh_index_url) { get_prh_index_url }
  let(:prh_targets_base) { get_prh_targets_base }
  let(:prh_new_url) { prh_targets_base + '/new' }

  feature "CRUD operations for hooks" do
    before(:all) do
      wipe_pre_receive_hooks
      ensure_repo_exists(@repo_name, auto_init: true)
      ensure_repo_exists("pre-receive-hooks-#{@timestamp}")
      add_fixture_file_to_repo("pre-receive-hooks-#{@timestamp}", src_filename:'reject-all.sh', dst_filename:'reject-all.sh')
    end

    context "With no hooks defined" do
      scenario "displays blank slate" do
        visit(prh_index_url)
        blank_slate_message = 'No pre-receive hooks have been created yet'
        expect(page).to have_content(blank_slate_message)
      end
    end

    context "With hooks defined" do
      before(:all) do
        resp = create_pre_receive_hook("reject-all-#{@timestamp}", 'reject-all.sh', repo_name:"pre-receive-hooks-#{@timestamp}")
        json = JSON.parse(resp.body)
        @hook_id = json['id']
        @hook_name = json['name']
      end

      before(:each) do
        login
        visit(prh_index_url)
      end

      scenario "admin buttons are visible" do
        expect(page).to have_content('Add pre-receive hook')
        expect(page).to have_content('Manage environments')
      end

      scenario "existing hooks are visible" do
        expect(page).to have_content("reject-all-#{@timestamp}")
      end

      scenario "existing hooks have links to relevant audit logs" do
        scoped_node = find(".pre-receive-hook-list")
        path = "pre_receive_hook_id%3A#{@hook_id}"
        expect(scoped_node).to have_link("Audit log", href: /.*#{path}.*/)
      end

      # this this needs some fixing up so it's not order dependant
      scenario "deleting a hook" do
        edit_path = "//div/a[contains(@href,'#{prh_targets_base}/#{@hook_id}')]"
        delete_button = page.find(:xpath, edit_path).sibling("details").find("summary")

        delete_button.click
        sleep 0.75

        page.find_button("Yes, delete #{@hook_name}", visible: false).trigger("click")

        blank_slate_message = 'No pre-receive hooks have been created yet'
        expect(page).to have_content(blank_slate_message)
      end
    end

    context "When adding a new hook" do
      before(:each) do
        visit(prh_index_url)
        click_on 'Add pre-receive hook'
        sleep 0.5
      end

      after(:all) do
        delete_pre_receive_hook("reject-all-#{@timestamp}")
      end

      scenario "requires name field to be populated" do
        click_on "Add pre-receive hook"
        sleep 0.5
        expect(page).to have_content("Name can't be blank")
      end

      scenario "requires a repo to be selected" do
        fill_in("pre_receive_hook_target[hook_attributes][name]", with: "hook test")
        click_on "Add pre-receive hook"
        expect(page).to have_content("Repository can't be blank")
      end

      scenario "requires a hook script to be selected" do
        fill_in("pre_receive_hook_target[hook_attributes][name]", with: "hook test")
        click_on_hook_repository_dropdown
        fill_in("Search repositories", with: "pre-receive-hooks-#{@timestamp}")
        sleep 0.1
        page.find(".css-truncate-target", text:"#{@user}/pre-receive-hooks-#{@timestamp}").click
        click_on "Add pre-receive hook"
        expect(page).to have_content("Script can't be blank")
      end

      scenario "correctly redirects upon successful hook creation" do
        fill_in("pre_receive_hook_target[hook_attributes][name]", with: "hook test")
        click_on_hook_repository_dropdown
        fill_in("Search repositories", with: "pre-receive-hooks-#{@timestamp}")
        sleep 0.1
        page.find(".css-truncate-target", text:"#{@user}/pre-receive-hooks-#{@timestamp}").click
        sleep 0.5
        click_on_select_file_dropdown
        sleep 0.1
        page.find(".select-menu-item-text", text: "reject-all.sh").click
        click_on "Add pre-receive hook"
        expect(current_path).to eql(prh_index_url)
      end
    end

    context "When editing hook enforcement options - admin override, hooks enabled for all repos" do
      before(:all) do
        wipe_pre_receive_hooks
      end

      before(:each) do
        resp = create_pre_receive_hook("reject-all-#{@timestamp}", 'reject-all.sh', repo_name:"pre-receive-hooks-#{@timestamp}")
        json = JSON.parse(resp.body)
        @hook_id = json['id']
        @hook_name = json['name']
        visit("#{prh_targets_base}/#{@hook_id}")
        check("pre_receive_hook_target_hook_attributes_notfinal")
        click_on "Save changes"
      end

      after(:each) do
        delete_pre_receive_hook("reject-all-#{@timestamp}")
      end

      scenario "allows an admin user to change hook settings" do
        visit("/#{@user}/pre-receive-hooks-#{@timestamp}/settings/hooks")
        sleep 5
        click_on_enabled_dropdown
        sleep 5
        expect(page).to have_css('span.select-menu-item-heading', :text => "Disabled", :visible => true)
      end

    end

    context "When editing hook enforcement options - admin override disabled, hooks enabled for all repos" do
      before(:all) do
        wipe_pre_receive_hooks
      end

      before(:each) do
        resp = create_pre_receive_hook("reject-all-#{@timestamp}", 'reject-all.sh', repo_name:"pre-receive-hooks-#{@timestamp}")
        json = JSON.parse(resp.body)
        @hook_id = json['id']
        @hook_name = json['name']
      end

      after(:each) do
        delete_pre_receive_hook("reject-all-#{@timestamp}")
      end

      scenario "prevents an admin user from changing hook settings" do
        visit("/#{@user}/pre-receive-hooks-#{@timestamp}/settings/hooks")
        #expect(page).to have_content("reject-all-#{@timestamp}")
        click_on_enabled_dropdown
        expect(page).to_not have_css('span.select-menu-item-heading', :text => "Disabled", :visible => true)
      end

    end

    context "When editing hook enforcement options - admin override disabled, hooks not enforced for all repos" do
      before(:all) do
        wipe_pre_receive_hooks
      end

      before(:each) do
        resp = create_pre_receive_hook("reject-all-#{@timestamp}", 'reject-all.sh', repo_name:"pre-receive-hooks-#{@timestamp}")
        json = JSON.parse(resp.body)
        @hook_id = json['id']
        @hook_name = json['name']
        visit("#{prh_targets_base}/#{@hook_id}")
        uncheck "pre_receive_hook_target_hook_attributes_enable"
        click_on "Save changes"
      end

      after(:each) do
        delete_pre_receive_hook("reject-all-#{@timestamp}")
      end

      scenario "does not enable the hook on all repos" do
        visit("/#{@user}/pre-receive-hooks-#{@timestamp}/settings/hooks")
        expect(page).to_not have_content("reject-all-#{@timestamp}")
      end

    end

    context "When editing hook enforcement options - admin override enabled, hooks not enforced for all repos" do
      before(:all) do
        wipe_pre_receive_hooks
      end

      before(:each) do
        resp = create_pre_receive_hook("reject-all-#{@timestamp}", 'reject-all.sh', repo_name:"pre-receive-hooks-#{@timestamp}")
        json = JSON.parse(resp.body)
        @hook_id = json['id']
        @hook_name = json['name']
        visit("#{prh_targets_base}/#{@hook_id}")
        check "pre_receive_hook_target_hook_attributes_notfinal"
        uncheck "pre_receive_hook_target_hook_attributes_enable"
        click_on "Save changes"
      end

      after(:each) do
        delete_pre_receive_hook("reject-all-#{@timestamp}")
      end

      scenario "allows an admin user to enable the hook" do
        visit("/#{@user}/pre-receive-hooks-#{@timestamp}/settings/hooks")
        #expect(page).to have_content("reject-all-#{@timestamp}")
        click_on_disabled_dropdown
        expect(page).to have_css('span.select-menu-item-heading', :text => "Enabled", :visible => true)
      end

    end

  end

  feature "CRUD operations for pre-receive hook environments" do
    let(:manage_environments_path) { get_manage_environments_path }

    before(:all) do
      wipe_pre_receive_hooks
      ensure_repo_exists("prh-#{@timestamp}")
      add_fixture_file_to_repo("prh-#{@timestamp}", src_filename:'reject-all.sh', dst_filename:'reject-all.sh')
    end

    before(:each) do
      visit(prh_index_url)
      click_on("Manage environments")
    end

    after(:all) do
      wipe_pre_receive_environments
    end

    context "clicking through to manage environments" do
      scenario "directs to management view" do
        sleep 0.5
        expect(current_path).to eql(manage_environments_path)
        expect(page).to have_content("Manage pre-receive hook environments")
      end
    end

    context "when adding an environment", :slow do
      let(:environment_name) { "testenv-#{new_timestamp}" }

      before(:each) do
        click_on("Add environment")
      end

      scenario "required fields are validated" do
        sleep 0.5
        click_on("Add environment")
        expect(page).to have_content("Name can't be blank")
        expect(page).to have_content("Image URL can't be blank")
      end

      scenario "a valid environment can be created" do
        fill_in("Environment name", with: environment_name)
        fill_in("Upload environment from a URL", with: "https://github-enterprise.s3.amazonaws.com/environments/pre-receive-qa.alpine-3.3.tar.gz")
        click_on "Add environment"
        expect(page).to have_content("Successfully created environment")
      end

      scenario "a newly created environment is reported as downloaded and ready" do
        fill_in("Environment name", with: environment_name)
        fill_in("Upload environment from a URL", with: "https://github-enterprise.s3.amazonaws.com/environments/pre-receive-qa.alpine-3.3.tar.gz")
        click_on "Add environment"
        scope = find('li.listgroup-item.pre-receive-hook-list', text: environment_name)
        expect(scope).to have_content("Environment downloaded and ready", wait: 20)
      end

      scenario "creating a hook in a new environment bumps the use count" do
        fill_in("Environment name", with: environment_name)
        fill_in("Upload environment from a URL", with: "https://github-enterprise.s3.amazonaws.com/environments/pre-receive-qa.alpine-3.3.tar.gz")
        click_on "Add environment"
        scope = find('li.listgroup-item.pre-receive-hook-list', text: environment_name)
        # wait for it to be ready before trying to use it
        expect(scope).to have_content("Environment downloaded and ready", wait: 20)
        visit(prh_index_url)
        click_on("Add pre-receive hook")
        fill_in("Hook name", with: "hook using #{environment_name}")
        click_on_environment_dropdown
        sleep 0.1
        scope = find('div.select-menu-list')
        scope.find('div.select-menu-item-text', text: environment_name).click
        click_on_hook_repository_dropdown
        fill_in("Search repositories", with: "prh-#{@timestamp}")
        page.find(".css-truncate-target", text:"#{@user}/prh-#{@timestamp}").click
        sleep 0.5
        click_on_select_file_dropdown
        page.find(".select-menu-item-text", text: "reject-all.sh").click
        click_on("Add pre-receive hook")
        click_on("Manage environments")
        scope = find('li.listgroup-item.pre-receive-hook-list', text: environment_name)
        expect(scope).to have_content("1 pre-receive hooks")
      end
    end

    context "when editing an environment" do
      let(:environment_name) { "testenv-#{new_timestamp}" }
      let(:env_id) { get_prh_env_id(environment_name) }

      before(:each) do
        click_on("Add environment")
        fill_in("Environment name", with: environment_name)
        fill_in("Upload environment from a URL", with: "https://github-enterprise.s3.amazonaws.com/environments/pre-receive-qa.alpine-3.3.tar.gz")
        click_on "Add environment"
        scope = find('li.listgroup-item.pre-receive-hook-list', text: environment_name)
        # wait for it to be ready before trying to use it
        expect(scope).to have_content("Environment downloaded and ready", wait: 20)
      end

      scenario "setting an invalid URL results in download failure" do
        # hack until bug is fixed
        page.evaluate_script 'window.location.reload()'
        scope = find('li.listgroup-item.pre-receive-hook-list', text: environment_name)
        find(:xpath, "//a[@href='#{manage_environments_path}/#{env_id}']").click
        fill_in("Upload environment from a URL", with: "ht://invali.d")
        click_on("Update environment")
        expect(scope).to have_content("Download failed.")
      end

      scenario "correcting an invalid URL results in successful download" do
        page.evaluate_script 'window.location.reload()'
        scope = find('li.listgroup-item.pre-receive-hook-list', text: environment_name)
        find(:xpath, "//a[@href='#{manage_environments_path}/#{env_id}']").click

        fill_in("Upload environment from a URL", with: "ht://invali.d")
        click_on("Update environment")
        if scope.has_content?("Download is in progress")
          # Sometimes we can hit this before the download has failed
          sleep 2
        end
        expect(scope).to have_content("Download failed.")
        scope = find('li.listgroup-item.pre-receive-hook-list', text: environment_name)
        find(:xpath, "//a[@href='#{manage_environments_path}/#{env_id}']").click
        fill_in("Upload environment from a URL", with: "https://github-enterprise.s3.amazonaws.com/environments/pre-receive-qa.alpine-3.3.tar.gz")
        click_on("Update environment")
        sleep 2
        expect(scope).to have_content("Environment downloaded and ready", wait: 20)
      end
    end

    context "when deleting an environment" do
      let(:environment_name) { "testenv-#{new_timestamp}" }
      let(:env_id) { get_prh_env_id(environment_name) }

      before(:all) do
        wipe_pre_receive_hooks
      end

      before(:each) do
        click_on("Add environment")
        fill_in("Environment name", with: environment_name)
        fill_in("Upload environment from a URL", with: "https://github-enterprise.s3.amazonaws.com/environments/pre-receive-qa.alpine-3.3.tar.gz")
        click_on "Add environment"
        scope = find('li.listgroup-item.pre-receive-hook-list', text: environment_name)
        # wait for it to be ready before trying to use it
        expect(scope).to have_content("Environment downloaded and ready", wait: 20)
        page.evaluate_script 'window.location.reload()'
      end

      scenario "displays modal dialog to confirm" do
        env_delete_button.click
        scope = find("details-dialog[aria-label='Delete #{environment_name}?']",
                       visible: false)
        expect(scope).to have_content("cannot be undone")
      end

      scenario "does not delete if modal is dismissed" do
        env_delete_button.click
        scope = find("details-dialog")
        scope.find('button[aria-label="Close dialog"]').click
        page.evaluate_script 'window.location.reload()'
        expect(page).to have_content(environment_name)
      end

      scenario "deletes when confirmed" do
        env_delete_button.click
        click_on "Yes, delete #{environment_name}"
        page.evaluate_script 'window.location.reload()'
        expect(page).to_not have_content(environment_name)
      end

      scenario "prevents delete if hooks are attached to environment" do
        if GHE_TARGET_VERSION >= SemVer.parse('3.9.0')
          visit("/enterprises/github/settings/hooks")
        else
          visit("admin/pre_receive_hook_targets")
        end
        click_on("Add pre-receive hook")
        fill_in("Hook name", with: "hook using #{environment_name}")
        click_on_environment_dropdown
        scope = find('div.select-menu-modal')
        scope.find('div.select-menu-item-text', text: environment_name).click
        click_on_hook_repository_dropdown
        fill_in("Search repositories", with: "prh-#{@timestamp}")
        sleep 0.1
        page.find(".css-truncate-target", text:"#{@user}/prh-#{@timestamp}").click
        sleep 5
        click_on_select_file_dropdown
        sleep 5
        page.find(".select-menu-item-text", text: "reject-all.sh").click
        sleep 0.1
        click_on("Add pre-receive hook")
        click_on("Manage environments")
        scope = find('li.listgroup-item.pre-receive-hook-list', text: environment_name)
        expect(scope).to have_content("1 pre-receive hooks")
        scope = find("div[data-url='#{manage_environments_path}/#{env_id}/environment_actions']")
        expect(scope).to have_selector('button[aria-label="Environment can not be deleted while in use by pre-receive hooks"]')
      end
    end

  end
end
